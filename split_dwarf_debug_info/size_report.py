#!/usr/bin/env python3
"""Print a markdown table of the outputs Bazel declares for each variant.

Declared outputs are exactly what a remote cache receives, so the "declared
total" column approximates the per-target upload volume.
"""

import argparse
import os
import sys

from elf_debug_info import find_dwo_names, is_debug_section, load_variant, read_sections

_MIB = 1024 * 1024


def _mib(size):
    return f"{size / _MIB:.1f} MiB"


def _total_size(paths):
    return sum(os.path.getsize(p) for p in paths)


def _row(variant):
    objects = variant.files_with_suffix(".o")
    dwos = variant.files_with_suffix(".dwo")
    libraries = variant.files_with_suffix(".so")

    library_debug_size = sum(
        s.size_on_disk
        for path in libraries
        for s in read_sections(path)
        if is_debug_section(s)
    )
    referenced_dwos = set()
    for path in objects + libraries:
        referenced_dwos.update(find_dwo_names(read_sections(path)))
    undeclared_dwos = [
        name
        for name in referenced_dwos
        if not any(name == dwo or name.endswith("/" + dwo) for dwo in dwos)
    ]

    return [
        variant.name,
        ", ".join(variant.features),
        "yes" if variant.fission else "no",
        _mib(_total_size(objects)),
        _mib(_total_size(dwos)) if dwos else "-",
        _mib(_total_size(libraries)),
        _mib(library_debug_size),
        _mib(_total_size(variant.files)),
        str(len(undeclared_dwos)) if undeclared_dwos else "-",
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="+", help="JSON manifests produced by debug_info_variant")
    args = parser.parse_args()

    header = [
        "Variant",
        "Features",
        "--fission",
        ".o",
        ".dwo (declared)",
        ".so",
        ".so debug sections",
        "Declared total",
        "Undeclared .dwo refs",
    ]
    rows = [header] + [_row(load_variant(m)) for m in args.manifests]
    widths = [max(len(row[i]) for row in rows) for i in range(len(header))]

    def format_row(row):
        return "| " + " | ".join(cell.ljust(w) for cell, w in zip(row, widths)) + " |"

    print(format_row(header))
    print("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for row in rows[1:]:
        print(format_row(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
