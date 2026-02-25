def _simple_repo_rule_impl(ctx):
    ctx.symlink(ctx.attr.build_file, "BUILD")

simple_repo_rule = repository_rule(
    implementation = _simple_repo_rule_impl,
    attrs = {
        "build_file": attr.label(allow_single_file = True),
    },
)

def _my_extension_impl(ctx):
    simple_repo_rule(
        name = "my_repo",
        build_file = "//:repo_contents.BUILD",
    )
    simple_repo_rule(
        name = "platforms_repo",
        build_file = "//:platforms_repo_contents.BUILD",
    )

my_extension = module_extension(
    implementation = _my_extension_impl,
)
