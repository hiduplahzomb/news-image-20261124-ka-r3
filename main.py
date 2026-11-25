#!/usr/bin/env python3
"""make.fun entry: Sum up 24 November's world news in one image.

Copies the pre-rendered entry.png shipped in this repository to the
output directory (MAKEFUN_OUTPUT_DIR, or /output when unset), then
reads the copy back and verifies it is byte-identical to the source.
Exits non-zero on any mismatch. Standard library only, no network.
"""
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as f:
        expected = f.read()
    shutil.copyfile(SOURCE, dest)
    with open(dest, "rb") as f:
        actual = f.read()
    if actual != expected:
        print("error: copied entry.png differs from source", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, verified identical)" % (dest, len(actual)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
