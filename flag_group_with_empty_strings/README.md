# Flag groups with empty strings in `expand_if_*`
The key takeaway from this example is that passing an empty string rather than
`None` into a `flag_group()` constructor has unexpected behavior. More
specifically, the empty string is happily literally treated like a string of
nothing: `expand_if_available` is always false, and `expand_if_not_available`
is always true, and `expand_if_available` takes precedence over both
`expand_if_not_available` and `iterate_over`.

## Notes
* If `iterate_over` is an empty string, this error is produced:
  ```
  Compiling hello_world.c failed: failed to generate compile command for rule '//:hello_world: Invalid toolchain configuration: Cannot find variable named ''.
  ```
* If `expand_if_available` is an empty string, Bazel doesn't complain and the
  flag disappears from the compiler invocation.
* If `expand_if_not_available` is an empty string, Bazel doesn't complain and
  the flag remains in the compiler invocation.
* If both `expand_if_available` and `expand_if_not_available` are empty strings,
  the flag disappears from the compiler invocation.
* If `expand_if_available` and `iterate_over` are both empty strings, Bazel
  no longer complains and just drops the flag from the compiler invocation.
* If `expand_if_not_available` and `iterate_over` are empty strings, Bazel
  complains again with the following error:
  ```
  Compiling xy_foo.cc failed: failed to generate compile command for rule '//:xy_foo: Invalid toolchain configuration: Cannot find variable named ''.
  ```
