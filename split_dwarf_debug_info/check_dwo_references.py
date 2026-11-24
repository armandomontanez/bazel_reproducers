#!/usr/bin/env python3
"""Fail if split DWARF skeletons reference .dwo files Bazel didn't declare.

Undeclared outputs are never uploaded to a remote cache, are not collected by
remote executors, and are discarded along with the sandbox. A debugger that
follows DW_AT_dwo_name from a cached or remotely built artifact finds nothing.
"""

import argparse
import sys

from elf_debug_info import find_dwo_names, load_variant, read_sections


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="JSON manifest produced by debug_info_variant")
    args = parser.parse_args()

    variant = load_variant(args.manifest)
    declared_dwos = variant.files_with_suffix(".dwo")
    print(f"Variant: {variant.name} (features: {', '.join(variant.features)})")
    print(f"Declared .dwo files: {declared_dwos or 'none'}")

    missing = False
    for path in variant.files_with_suffix(".o") + variant.files_with_suffix(".so"):
        for dwo_name in sorted(find_dwo_names(read_sections(path))):
            declared = any(
                dwo_name == dwo or dwo_name.endswith("/" + dwo) for dwo in declared_dwos
            )
            print(f"{path} -> {dwo_name}: {'declared' if declared else 'UNDECLARED'}")
            missing |= not declared

    if missing:
        print("\nERROR: Debug info points at .dwo files Bazel does not track.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
