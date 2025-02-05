_FLAG_REPO_BUILD = """
load("@bazel_skylib//rules:common_settings.bzl", "bool_flag")

bool_flag(
    name = "external_flag",
    build_setting_default = False,
    visibility = ["//visibility:public"],
)
"""

def _flag_repo_impl(ctx):
    ctx.file("BUILD.bazel")
    ctx.file("external_flag/BUILD.bazel", content=_FLAG_REPO_BUILD)

flag_repo = repository_rule(
    implementation = _flag_repo_impl,
)
