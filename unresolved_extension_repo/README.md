# Repo rule exposed by module extension evaluates

Several users have reported cases where a repository fails to exist under the following conditions:

* Bzlmod is in use.
* A module extension is in use.
* A repository is exposed by the module extension to the current module.
* A build is invoked setting a flag inside the exposed repository, or pointing the flag at something inside the repository.

Bazel fails to find the repo, throwing an error like the following:

```
ERROR: com.google.devtools.build.lib.packages.BuildFileNotFoundException: no such package '@@[unknown repo 'my_repo' requested from @@]//': The repository '@@[unknown repo 'my_repo' requested from @@]' could not be resolved: No repository visible as '@my_repo' from main repository
```

## Notes

*This example currently does NOT reproduce the error.*

```
$ bazelisk build --platforms=@platforms_repo//:my_platform //:hello_world
```

```
$ bazelisk build --@my_repo//:my_flag=//:hello_world //:hello_world
```

HOWEVER, this **does** reproduce for `bazel info` when using `--platforms`:
```
$ bazelisk info --platforms=@platforms_repo//:my_platform
ERROR: com.google.devtools.build.lib.packages.BuildFileNotFoundException: no such package '@@platforms_repo//': The repository '@@platforms_repo' could not be resolved: Repository '@@platforms_repo' is not defined
```

Note that `--@my_repo//:my_flag=//:hello_world` does NOT fail under `bazel info`.
