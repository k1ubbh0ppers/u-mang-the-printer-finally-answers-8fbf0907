#!/usr/bin/env python3
"""The printer gets the last word — a make.fun one-line entry.

This script drops a single comeback from a long-suffering office
printer into entry.txt, in whatever folder the grader points to
through MAKEFUN_OUTPUT_DIR (or /output when that is not set).
The comeback itself lives right here in the file; the script needs
no network, no files, and nothing beyond the standard library.

The joke: the machine has swallowed enough paper, and this time it
admits it — it did not jam, it ate the document, and it has opinions
about the taste.

The entry must clear the gate: between 1 and 240 characters, exactly
one line, something besides blank space, and ASCII all the way down.
"""

import os
import sys
from pathlib import Path

ENTRY = "I didn't jam. I ate your document. It tasted like urgency and poor planning."

LOWER = 1
UPPER = 240


def gate_failures(line: str) -> list[str]:
    """List every way the line misses the gate; no items means go."""
    complaints: list[str] = []
    if not line.isascii():
        complaints.append("entry must be ASCII only")
    if "\n" in line or "\r" in line:
        complaints.append("entry must fit on one line")
    if line.strip() == "":
        complaints.append("entry is blank")
    if not LOWER <= len(line) <= UPPER:
        complaints.append(f"got {len(line)} characters; the gate allows 1 to 240")
    return complaints


def publish_entry(line: str) -> int:
    """Check the line, then save it with no newline at the end."""
    failed = gate_failures(line)
    if failed:
        for complaint in failed:
            print(f"rejected: {complaint}", file=sys.stderr)
        return 1
    if "MAKEFUN_OUTPUT_DIR" in os.environ:
        out_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    else:
        out_dir = Path("/output")
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    (out_dir / "entry.txt").write_text(line, encoding="utf-8")
    print(line)
    print(f"length: {len(line)} characters")
    return 0


def main() -> int:
    return publish_entry(ENTRY)


if __name__ == "__main__":
    sys.exit(main())
