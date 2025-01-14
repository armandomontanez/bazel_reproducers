load("@bazel_skylib//rules:common_settings.bzl", "BuildSettingInfo")

def _symlink_with_toolchain_impl(ctx):
    test_script = ctx.actions.declare_file(ctx.label.name)
    if not ctx.toolchains["//:arbitrary_toolchain"].flag_value:
        fail("Toolchain flag not flipped when symlinking from exec")
    ctx.actions.symlink(
        output = test_script,
        target_file = ctx.executable.src,
        is_executable = True,
    )
    return DefaultInfo(executable=test_script)

symlink_with_toolchain = rule(
    implementation = _symlink_with_toolchain_impl,
    attrs = {
        "src": attr.label(allow_single_file=True, executable=True, cfg="exec"),
    },
    toolchains = ["//:arbitrary_toolchain"],
)

def _nop_test_impl(ctx):
    test_script = ctx.actions.declare_file(ctx.label.name)
    if not ctx.toolchains["//:arbitrary_toolchain"].flag_value:
        fail("Toolchain flag not flipped when symlinking from target")
    ctx.actions.symlink(
        output = test_script,
        target_file = ctx.executable.tool,
        is_executable = True,
    )
    return DefaultInfo(executable=test_script)

nop_test = rule(
    implementation = _nop_test_impl,
    attrs = {
        "tool": attr.label(allow_single_file=True, executable=True, cfg="exec"),
    },
    test = True,
    toolchains = ["//:arbitrary_toolchain"],
)


def _my_toolchain_impl(ctx):
    if not ctx.attr.config_flag[BuildSettingInfo].value:
        fail("The configuration flag didn't apply as expected when evaluating the toolchain")
    return platform_common.ToolchainInfo(
        flag_value = ctx.attr.config_flag[BuildSettingInfo].value,
    )

my_toolchain = rule(
    implementation = _my_toolchain_impl,
    attrs = {
        "config_flag": attr.label(mandatory=True),
    },
)
