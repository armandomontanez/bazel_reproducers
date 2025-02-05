def _exec_shim_impl(ctx):
    files = []
    for file in ctx.attr.target[DefaultInfo].files.to_list():
        linked_file = ctx.actions.declare_symlink(ctx.label.name + "_" + file.basename)
        ctx.actions.symlink(
            file,
            linked_file,
        )
        files.append(linked_file)
    file_depset = depset(
        direct = files,
        transitive = [ctx.attr.target[DefaultInfo].files],
    )
    return [
        DefaultInfo(
            files = file_depset,
        ),
    ]

exec_shim = rule(
    implementation = _exec_shim_impl,
    attrs = {
        "target": attr.label(cfg = "exec"),
    },
)
