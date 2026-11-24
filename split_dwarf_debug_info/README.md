# Split DWARF without `--fission`

Explores a proposed trick for reducing the volume of sanitizer debug info
uploaded to a remote cache:

```
bazel build //my:target --compilation_mode=dbg --fission=no --copt=-gsplit-dwarf
```

The idea is that the compiler writes both a `.o` and a `.dwo`, but Bazel only
declares (and therefore only uploads) the `.o`. A related claim is that this
leaves the `.o`/`.so` "untainted" by absolute paths in debug info.

The same header-free, template-heavy source file (`debug_bloat.cc`) is built
into a Linux x86_64 shared library several times, each with a different set of
features from the toolchain in `//toolchain`:

| Feature                    | Flags                                    |
|----------------------------|------------------------------------------|
| `asan` / `tsan`            | `-fsanitize=address` / `-fsanitize=thread` |
| `full_debug_info`          | `-g`                                     |
| `line_tables_only`         | `-gline-tables-only`                     |
| `split_dwarf_copt`         | `-gsplit-dwarf`, without `--fission`     |
| `relative_compilation_dir` | `-ffile-compilation-dir=.`               |
| `compress_debug_sections`  | `-gz=zlib` (compile and link)            |

`native_fission*` variants instead use `--fission=yes`, which drives the
builtin `per_object_debug_info` feature. Every variant is built through a
transition to `--compilation_mode=dbg` and `//platforms:linux_x86_64` so the
checks below can run on the host. Linux ELF is required; Mach-O silently
ignores `-gsplit-dwarf`.

## Reproducer steps
```
$ bazel test //...
$ bazel test //:size_report --test_output=all
```

* `//:<variant>_hermeticity_test` fails if the declared outputs embed paths
  from the build environment (output base, sandbox, execroot). Compressed debug
  sections are decompressed first; `-gz` hides paths from a naive `strings`.
* `//:<variant>_dwo_references_test` fails if split DWARF skeletons point at
  `.dwo` files that Bazel didn't declare.
* `//:size_report` prints the table below. "Declared total" is what a remote
  cache receives for the target.

## Results
Built on macOS (arm64) with the default `darwin-sandbox`:

| Variant                        | `.o`     | `.dwo` (declared) | `.so`    | `.so` debug sections | Declared total | Undeclared `.dwo` refs |
|--------------------------------|----------|-------------------|----------|----------------------|----------------|------------------------|
| no_debug_info                  | 14.0 MiB | -                 | 10.4 MiB | 0.0 MiB              | 24.4 MiB       | -                      |
| full_debug_info                | 26.2 MiB | -                 | 20.1 MiB | 9.8 MiB              | 46.4 MiB       | -                      |
| full_debug_info_tsan           | 30.7 MiB | -                 | 20.2 MiB | 9.2 MiB              | 50.8 MiB       | -                      |
| full_debug_info_relative       | 26.2 MiB | -                 | 20.1 MiB | 9.8 MiB              | 46.4 MiB       | -                      |
| compressed_debug_info          | 17.3 MiB | -                 | 11.6 MiB | 1.2 MiB              | 28.9 MiB       | -                      |
| compressed_debug_info_relative | 17.3 MiB | -                 | 11.6 MiB | 1.2 MiB              | 28.9 MiB       | -                      |
| line_tables_only_relative      | 17.5 MiB | -                 | 13.2 MiB | 2.9 MiB              | 30.7 MiB       | -                      |
| split_dwarf_copt               | 20.4 MiB | -                 | 16.1 MiB | 5.8 MiB              | 36.5 MiB       | 1                      |
| split_dwarf_copt_relative      | 20.4 MiB | -                 | 16.1 MiB | 5.8 MiB              | 36.5 MiB       | 1                      |
| native_fission                 | 20.4 MiB | 6.9 MiB           | 16.7 MiB | 6.4 MiB              | 44.0 MiB       | -                      |
| native_fission_relative        | 20.4 MiB | 6.9 MiB           | 16.7 MiB | 6.4 MiB              | 44.0 MiB       | -                      |

Hermeticity failures: `full_debug_info`, `full_debug_info_tsan`,
`compressed_debug_info`, `split_dwarf_copt`, and `native_fission`. Every
`*_relative` variant passes.

## Notes
* The trick does reduce what's uploaded: 36.5 MiB vs 46.4 MiB for `-g`. The
  `.dwo` is never declared, so it's discarded with the sandbox even for local
  builds (`bazel-out/.../_objs/libsplit_dwarf_copt.so/` has no `.dwo`). The
  `.o` and `.so` still point at it via `DW_AT_dwo_name`, so debugging any
  artifact built this way only has line tables.
* Split DWARF does not remove absolute paths. The skeleton unit keeps
  `DW_AT_comp_dir`, which on a macOS exec platform is the per-action sandbox
  (`.../sandbox/darwin-sandbox/<N>/execroot/_main`). The `<N>` changes between
  actions, so these outputs aren't even reproducible on the same machine.
  `-ffile-compilation-dir=.` is what fixes this, with or without split DWARF.
* On a Linux exec platform `CppCompileAction` sets `PWD=/proc/self/cwd`, which
  clang/gcc record as the comp dir instead of `getcwd()`. The
  non-`relative` variants are expected to pass there (not verified here).
* Even `no_debug_info` contains absolute paths from the LLVM build machine
  (`/Volumes/Work/s/w/ir/...`), via the debug info of the prebuilt
  `libclang_rt.asan_static.a` that clang links into the shared library. These
  are reported as `prebuilt input` and don't fail the check, since they're the
  same everywhere this toolchain is used.
* `.o` files barely shrink with `-gsplit-dwarf` (26.2 to 20.4 MiB) because the
  relocations for the remaining debug sections stay in the object.
* Native fission links with `-Wl,--gdb-index`, which replaces the skeleton's
  `.debug_gnu_pubnames`/`.debug_gnu_pubtypes` with a larger `.gdb_index`.
* `-gline-tables-only` (enough for symbolized sanitizer reports) and `-gz`
  shrink uploads more than the trick without leaving dangling `.dwo`
  references.
