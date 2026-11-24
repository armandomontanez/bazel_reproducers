"""Builds one debug info variant of //:debug_bloat.cc for Linux."""

load("@bazel_skylib//rules:native_binary.bzl", "native_test")
load("@rules_cc//cc:defs.bzl", "cc_binary")

def _linux_dbg_transition_impl(_settings, attr):
    return {
        "//command_line_option:compilation_mode": "dbg",
        "//command_line_option:fission": "yes" if attr.fission else "no",
        "//command_line_option:platforms": str(Label("//platforms:linux_x86_64")),
    }

_linux_dbg_transition = transition(
    implementation = _linux_dbg_transition_impl,
    inputs = [],
    outputs = [
        "//command_line_option:compilation_mode",
        "//command_line_option:fission",
        "//command_line_option:platforms",
    ],
)

def _debug_info_variant_impl(ctx):
    binary = ctx.attr.binary[0]
    output_groups = binary[OutputGroupInfo]
    artifacts = depset(transitive = [
        binary[DefaultInfo].files,
        getattr(output_groups, "compilation_outputs", depset()),
        getattr(output_groups, "dwo_files", depset()),
    ]).to_list()

    manifest = ctx.actions.declare_file(ctx.label.name + ".json")
    ctx.actions.write(
        output = manifest,
        content = json.encode_indent({
            "name": ctx.label.name,
            "features": ctx.attr.cc_features,
            "fission": ctx.attr.fission,
            "files": [artifact.short_path for artifact in artifacts],
        }),
    )
    return [DefaultInfo(
        files = depset([manifest]),
        runfiles = ctx.runfiles(files = [manifest] + artifacts),
    )]

_debug_info_variant = rule(
    implementation = _debug_info_variant_impl,
    attrs = {
        "binary": attr.label(cfg = _linux_dbg_transition, mandatory = True),
        "cc_features": attr.string_list(),
        "fission": attr.bool(),
    },
)

def debug_info_variant(name, features, fission = False):
    """Declares a variant of the debug_bloat shared library and its checks.

    Args:
        name: Name of the variant. Creates `:<name>` (a JSON manifest of every
            file Bazel declared for the variant), `:<name>_hermeticity_test`,
            and `:<name>_dwo_references_test`.
        features: Toolchain features from //toolchain to enable.
        fission: Whether to build with `--fission=yes`.
    """
    cc_binary(
        name = "lib{}.so".format(name),
        srcs = ["//:debug_bloat.cc"],
        copts = ["-std=c++17"],
        features = features,
        linkshared = True,
        tags = ["manual"],
    )

    _debug_info_variant(
        name = name,
        binary = ":lib{}.so".format(name),
        cc_features = features,
        fission = fission,
    )

    native_test(
        name = name + "_hermeticity_test",
        src = "//:check_hermeticity",
        args = ["$(rootpath :{})".format(name)],
        data = [":" + name],
    )

    native_test(
        name = name + "_dwo_references_test",
        src = "//:check_dwo_references",
        args = ["$(rootpath :{})".format(name)],
        data = [":" + name],
    )
