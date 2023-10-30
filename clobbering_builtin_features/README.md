# Clobbering builtin features
It turns out, the "empty" toolchain case isn't really "empty."

## Notes
* `alwayslink` Didn't do anything when the `features` list was empty.... But the
  binary still linked.
* Clobbering the `libraries_to_link` feature with a partial implementation
  reveals you can completely break toolchains simply by specifying a builtin
  feature name.
