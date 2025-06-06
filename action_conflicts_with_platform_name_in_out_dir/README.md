# Conflict between @local_config_platform//:host and @platforms//host
## Summary
When `--experimental_platform_in_output_dir` is enabled, any C++ compile
actions targeting `@local_config_platform//:host` will conflict with identical
actions targeting `@platforms//host`.

## Reproducing
Run the following command:
```
$ bazel build //...
```
Which produces the following output:
```
$ bazel build //...
WARNING: Build options --experimental_exclude_defines_from_exec_config, --experimental_exclude_starlark_flags_from_exec_config, --incompatible_bazel_test_exec_run_under, and 2 more have changed, discarding analysis cache (this can be expensive, see https://bazel.build/advanced/performance/iteration-speed).
ERROR: file '_objs/data_binary/main.o' is generated by these conflicting actions:
Label: //:data_binary
RuleClass: cc_binary rule
JavaActionClass: class com.google.devtools.build.lib.rules.cpp.CppCompileAction
Configuration: 1266988732fa9e033085170afb27b1844ac37e0321fb67d8ec9b375ebfc93f26, c80e5e0cf4f1be62db5504937d2ca971bc878717f37de07ce0f4f526e6bcd575
Mnemonic: CppCompile
Action key: 7dc6772ccd5192cbc39d0cc9e7e2b47cceb66fe50881d8e5b5904789885b71b5
Progress message: Compiling main.cc
Action describeKey: Compiling main.cc
  Command: external/rules_cc++cc_configure_extension+local_config_cc/cc_wrapper.sh
  Argument: -U_FORTIFY_SOURCE
  Argument: -fstack-protector
  Argument: -Wall
  Argument: -Wthread-safety
  Argument: -Wself-assign
  Argument: -Wunused-but-set-parameter
  Argument: -Wno-free-nonheap-object
  Argument: -fcolor-diagnostics
  Argument: -fno-omit-frame-pointer
  Argument: '-std=c++17'
  Argument: '-frandom-seed=bazel-out/darwin_x86_64-fastbuild/bin/_objs/data_binary/main.o'
  Argument: '-mmacosx-version-min=10.11'
  Argument: -MD
  Argument: -MF
  Argument: bazel-out/darwin_x86_64-fastbuild/bin/_objs/data_binary/main.d
  Argument: -iquote
  Argument: .
  Argument: -iquote
  Argument: bazel-out/darwin_x86_64-fastbuild/bin
  Argument: -iquote
  Argument: external/rules_cc+
  Argument: -iquote
  Argument: bazel-out/darwin_x86_64-fastbuild/bin/external/rules_cc+
  Argument: -iquote
  Argument: external/bazel_tools
  Argument: -iquote
  Argument: bazel-out/darwin_x86_64-fastbuild/bin/external/bazel_tools
  Argument: -c
  Argument: main.cc
  Argument: -o
  Argument: bazel-out/darwin_x86_64-fastbuild/bin/_objs/data_binary/main.o
  Argument: -no-canonical-prefixes
  Argument: -Wno-builtin-macro-redefined
  Argument: '-D__DATE__="redacted"'
  Argument: '-D__TIMESTAMP__="redacted"'
  Argument: '-D__TIME__="redacted"'

PrimaryInput: File:[/Users/amontanez/development/projects/armandomontanez_github/bazel_reproducers/action_conflicts_with_platform_name_in_out_dir[source]]main.cc
PrimaryOutput: File:[[<execution_root>]bazel-out/darwin_x86_64-fastbuild/bin]_objs/data_binary/main.o
Owner information: ConfiguredTargetKey{label=//:data_binary, config=BuildConfigurationKey[1266988732fa9e033085170afb27b1844ac37e0321fb67d8ec9b375ebfc93f26]}, ConfiguredTargetKey{label=//:data_binary, config=BuildConfigurationKey[c80e5e0cf4f1be62db5504937d2ca971bc878717f37de07ce0f4f526e6bcd575]}
MandatoryInputs: are equal
Outputs: are equal
Use --verbose_failures to see the command lines of failed build steps.
ERROR: file '_objs/data_binary/main.o' is generated by these conflicting actions:
Label: //:data_binary
RuleClass: cc_binary rule
JavaActionClass: class com.google.devtools.build.lib.rules.cpp.CppCompileAction
Configuration: 1266988732fa9e033085170afb27b1844ac37e0321fb67d8ec9b375ebfc93f26, c80e5e0cf4f1be62db5504937d2ca971bc878717f37de07ce0f4f526e6bcd575
Mnemonic: CppCompile
Action key: 7dc6772ccd5192cbc39d0cc9e7e2b47cceb66fe50881d8e5b5904789885b71b5
Progress message: Compiling main.cc
Action describeKey: Compiling main.cc
  Command: external/rules_cc++cc_configure_extension+local_config_cc/cc_wrapper.sh
  Argument: -U_FORTIFY_SOURCE
  Argument: -fstack-protector
  Argument: -Wall
  Argument: -Wthread-safety
  Argument: -Wself-assign
  Argument: -Wunused-but-set-parameter
  Argument: -Wno-free-nonheap-object
  Argument: -fcolor-diagnostics
  Argument: -fno-omit-frame-pointer
  Argument: '-std=c++17'
  Argument: '-frandom-seed=bazel-out/darwin_x86_64-fastbuild/bin/_objs/data_binary/main.o'
  Argument: '-mmacosx-version-min=10.11'
  Argument: -MD
  Argument: -MF
  Argument: bazel-out/darwin_x86_64-fastbuild/bin/_objs/data_binary/main.d
  Argument: -iquote
  Argument: .
  Argument: -iquote
  Argument: bazel-out/darwin_x86_64-fastbuild/bin
  Argument: -iquote
  Argument: external/rules_cc+
  Argument: -iquote
  Argument: bazel-out/darwin_x86_64-fastbuild/bin/external/rules_cc+
  Argument: -iquote
  Argument: external/bazel_tools
  Argument: -iquote
  Argument: bazel-out/darwin_x86_64-fastbuild/bin/external/bazel_tools
  Argument: -c
  Argument: main.cc
  Argument: -o
  Argument: bazel-out/darwin_x86_64-fastbuild/bin/_objs/data_binary/main.o
  Argument: -no-canonical-prefixes
  Argument: -Wno-builtin-macro-redefined
  Argument: '-D__DATE__="redacted"'
  Argument: '-D__TIMESTAMP__="redacted"'
  Argument: '-D__TIME__="redacted"'

PrimaryInput: File:[/Users/amontanez/development/projects/armandomontanez_github/bazel_reproducers/action_conflicts_with_platform_name_in_out_dir[source]]main.cc
PrimaryOutput: File:[[<execution_root>]bazel-out/darwin_x86_64-fastbuild/bin]_objs/data_binary/main.o
Owner information: ConfiguredTargetKey{label=//:data_binary, config=BuildConfigurationKey[1266988732fa9e033085170afb27b1844ac37e0321fb67d8ec9b375ebfc93f26]}, ConfiguredTargetKey{label=//:data_binary, config=BuildConfigurationKey[c80e5e0cf4f1be62db5504937d2ca971bc878717f37de07ce0f4f526e6bcd575]}
MandatoryInputs: are equal
Outputs: are equal
```
