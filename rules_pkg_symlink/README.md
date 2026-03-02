# Shared object symlink not created in pkg_tar

Reproducer showing that `pkg_mklink` does not generate the expected symlink
when `pkg_files` is used at any stage in the middle.

## Expected behavior

When building the archive with `pkg_files`, the archive should contain the
enumerated symlink.

## Actual behavior

The symlink is not generated or included in the pkg_tar output as expected.

## Reproducer steps
Conveniently available as a test in this reproducer:
```
$ bazel test //...
```

```
# Build the tar archive
$ bazel build //:broken_archive

# Extract and inspect the archive
$ tar -tzf bazel-bin/broken_archive.tar

# Expected to see both:
#   usr/lib/libmylib.so.1
#   usr/lib/libmylib.so -> libmylib.so.1
```
