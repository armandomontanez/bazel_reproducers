# Propagating flags to toolchains
This attempts to reproduce an issue where `.bazelrc` flags don't properly
control flags behind toolchains.
(https://github.com/bazelbuild/bazel/issues/22457#issuecomment-2338650148)

The root of the issue is that whenever a toolchain targets the exec platform,
`--experimental_exclude_starlark_flags_from_exec_config` prevents `.bazelrc`
or CLI-passed configuration flags to propagate to the exec platform toolchain
configuration.

This makes sense when you unpack it, but is very easy to trip over since users
likely expect that configuration flags passed from the CLI will apply to both
the target and exec toolchain when the two are the same.

It's possible that this nuanced dissonance is causing latent bugs where the
build behaviors of target artifacts and exec artifacts are *slightly* different.


## Simplified, concrete example
If you build `protoc` it could be slightly different than a `protoc` built
after an `exec` transition if you pass any flags via the CLI or `.bazelrc` that
affect how `protoc` is compiled.

## Workaround
The only known workaround is to specify an explicit exec platform and host
platform that are known to be identical.
