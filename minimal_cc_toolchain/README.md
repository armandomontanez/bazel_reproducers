# Minimal toolchain to build C/C++
This is NOT production ready. It simply forks the generated `local_config_cc`
external repository and is not hermetic by any means.

## Notes
* Simpler than a hermetic toolchain that is downloaded from somewhere, mostly
  because running `gcc` on most systems doesn't require extra flags to work.
* The actual `local_config_cc` has a TON of features, but works perfectly fine
  for this simple case with *none* of them, which is somewhat surprising.
* From this example, it's not obvious where to add custom flags that should be
  applied across all C/C++ actions.
* In this example, headers are included via `-isystem` (e.g.
  `-isystem xy_include`), which seems unexpected.