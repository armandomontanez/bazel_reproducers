# Protobuf imports from external repos broken in Bazel 8.0.0 + rules_python 1.0.0

Reproducer illustrating that the new default of
`--legacy_external_runfiles=False` as dictated by Bazel 8.0.0 is broken when
using rules_python v1.0.0.

## Reproducer steps

```
$ cd actual_repo
# Fails.
$ bazel test //...
# Passes.
$ bazel test //... --legacy_external_runfiles=True
```

