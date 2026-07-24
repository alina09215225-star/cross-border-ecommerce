#!/usr/bin/env python3
"""
Check whether an input file is suitable for deep course learning.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Check learning input readiness.")
    parser.add_argument("input", help="Path to transcript, notes, or markdown")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

    text = path.read_text(encoding="utf-8")
    length = len(text.strip())
    lines = len(text.splitlines())

    print("Deep learning input check")
    print(f"- file: {path}")
    print(f"- characters: {length}")
    print(f"- lines: {lines}")

    if length < 500:
        print("- verdict: too short for full deep-learning flow; use as context supplement")
    elif length < 3000:
        print("- verdict: usable for short-form deep learning")
    else:
        print("- verdict: good for full deep-learning flow")


if __name__ == "__main__":
    main()
