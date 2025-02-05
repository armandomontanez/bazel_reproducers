# Propagating flags to exec config
This reproduces an issue where `--experimental_propagate_custom_flag` doesn't
work as expected.
(https://github.com/bazelbuild/bazel/issues/22457#issuecomment-2338650148)

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
