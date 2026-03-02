#!/usr/bin/env python3
"""Check if a path exists in a tar archive."""

import argparse
import sys
import tarfile


def main():
    parser = argparse.ArgumentParser(
        description="Verify a path exists in a tar archive"
    )
    parser.add_argument("archive", help="Path to the tar archive")
    parser.add_argument("expected_path", help="Expected path in the archive")
    args = parser.parse_args()

    with tarfile.open(args.archive, "r:*") as tar:
        members = {member.name for member in tar.getmembers()}

        if args.expected_path not in members:
            print(f"ERROR: Path not found in archive: {args.expected_path}")
            print("\nArchive contents:")
            for name in sorted(members):
                print(f"  {name}")
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
