# Propagating flags to exec config
This reproduces an issue where `--experimental_propagate_custom_flag` doesn't
work as expected.
(https://github.com/bazelbuild/bazel/issues/22457#issuecomment-2338650148)

## Core findings

1. The label passed to `--experimental_propagate_custom_flag` must be FULLY
   qualified. This means both using the canonical repo name, AND expanding any
   labels that match the name of their parent directory (e.g. `//foo:foo`).
2. If a nonexistent flag is passed, Bazel doesn't emit any warning or error.

## Reproducer steps
```
# Fails unexpectedly.
$ bazel build //:foo_test
# Passes with workaround.
$ bazel build //:foo_test --config=workaround
```

## Workaround
Use fully qualified labels when using `--experimental_propagate_custom_flag`,
including both the canonical repository name AND expanding `foo:foo` if the
directory name matches the label name.
