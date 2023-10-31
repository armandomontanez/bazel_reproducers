# Feature with a name that contains special characters
A minimal example that illustrates what happens when you put special characters
in the name of a feature.

## Notes
* Feature names with "/" or ":" are rejected, but the names are only validated
  if they're added to a toolchain.
* It's possible to break feature names by starting with double dashes.
  If it's placed independently on a line like:

  ```
  build --features=--my+friendly-feature.flag
  ```

  It silently does nothing.
