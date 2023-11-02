# Enabling nonexistent features
In this example, a feature is explicitly enabled via the CLI despite not
actually existing anywhere.

## Notes
* Specifying `implies` on a toolchain feature triggers validation that ensures
  the feature exists in the first place.
* Specifying a nonexistent feature on the CLI silently does nothing.
