# Minimal toolchain with a new feature
Just a minimial toolchain that adds a feature with an arbitrary flag to ensure
nothing unexpected happens.

## Notes
* The new feature is only applied if `enabled = True` is set. Just specifying,
  indicating features default to disabled if `enabled` is unspecified.
* Specifying an arbitrary feature doesn't implicitly disable all builtin/default
  features.
