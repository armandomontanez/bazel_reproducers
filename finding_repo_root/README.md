Illustrates how to reference a file from the root Bazel workspace.

```
~/bazel_reproducers/finding_repo_root/inner_module$ bazel build //:echo_message
INFO: Analyzed target //:echo_message (5 packages loaded, 8 targets configured).
INFO: From Executing genrule //:echo_message:
This is the inner module!
INFO: Found 1 target...
Target //:echo_message up-to-date:
  bazel-bin/result.txt
INFO: Elapsed time: 2.491s, Critical Path: 0.10s
INFO: 2 processes: 1 internal, 1 darwin-sandbox.
INFO: Build completed successfully, 2 total actions
~/bazel_reproducers/finding_repo_root/inner_module$ cd ..
~/bazel_reproducers/finding_repo_root$ bazel build //:echo_message
INFO: Analyzed target //:echo_message (6 packages loaded, 9 targets configured).
INFO: From Executing genrule @@inner~override//:echo_message:
This is the outer module!
INFO: Found 1 target...
Target @@inner~override//:echo_message up-to-date:
  bazel-bin/external/inner~override/result.txt
INFO: Elapsed time: 2.284s, Critical Path: 0.08s
INFO: 2 processes: 1 internal, 1 darwin-sandbox.
INFO: Build completed successfully, 2 total actions
```
