#!/usr/bin/env python3
"""Fail if a variant's declared outputs embed paths from the build environment."""

import argparse
import sys

from elf_debug_info import BUILD_ENVIRONMENT, classify_path, find_absolute_paths, load_variant, read_sections


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="JSON manifest produced by debug_info_variant")
    args = parser.parse_args()

    variant = load_variant(args.manifest)
    print(f"Variant: {variant.name} (features: {', '.join(variant.features)})")

    nonhermetic = False
    for path in variant.files:
        sections = read_sections(path)
        found = find_absolute_paths(sections)
        print(f"\n{path}")
        if not found:
            print("  no absolute paths")
            continue
        for found_path, section_names in sorted(found.items()):
            kind = classify_path(found_path)
            compressed = any(s.compressed for s in sections if s.name in section_names)
            note = " (inside compressed sections)" if compressed else ""
            print(f"  [{kind}] {found_path}")
            print(f"      in {', '.join(sorted(section_names))}{note}")
            nonhermetic |= kind == BUILD_ENVIRONMENT

    if nonhermetic:
        print("\nERROR: Outputs embed absolute paths from the build environment.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
