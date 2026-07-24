#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def esc(text: str) -> str:
    out = []
    for ch in text:
        code = ord(ch)
        if ch in "\\{}":
            out.append("\\" + ch)
        elif ch == "\n":
            out.append("\\line ")
        elif code < 128:
            out.append(ch)
        else:
            signed = code if code < 32768 else code - 65536
            out.append(f"\\u{signed}?")
    return "".join(out)


def clean(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    return text


def row_text(line: str) -> list[str]:
    return [clean(c.strip()) for c in line.strip().strip("|").split("|")]


def emit_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = row_text(line)
        if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    result = []
    cols = max(len(r) for r in rows)
    cell_width = max(1600, int(9000 / cols))
    for r in rows:
        r += [""] * (cols - len(r))
        result.append("\\trowd\\trgaph120")
        pos = 0
        for _ in range(cols):
            pos += cell_width
            result.append(f"\\cellx{pos}")
        for c in r:
            result.append("\\intbl " + esc(c) + "\\cell ")
        result.append("\\row\n")
    return "".join(result)


def convert(md: str) -> str:
    out = [
        r"{\rtf1\ansi\ansicpg65001\deff0",
        r"{\fonttbl{\f0 Arial Unicode MS;}{\f1 Helvetica;}}",
        r"{\colortbl;\red46\green116\blue181;\red31\green77\blue120;\red20\green32\blue46;\red95\green105\blue118;}",
        "\n",
    ]
    in_code = False
    code_lines: list[str] = []
    table_lines: list[str] = []

    def flush_table():
        nonlocal table_lines
        if table_lines:
            out.append(emit_table(table_lines))
            table_lines = []

    def flush_code():
        nonlocal code_lines
        if code_lines:
            out.append(r"\pard\sa160\sb120\cf3\f0\fs20 " + esc("\n".join(code_lines)) + r"\par" + "\n")
            code_lines = []

    for raw in md.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_table()
            if in_code:
                in_code = False
                flush_code()
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines.append(stripped)
            continue
        flush_table()
        if not stripped:
            continue
        if stripped.startswith("# "):
            out.append(r"\pard\sa220\sb260\b\cf3\f0\fs36 " + esc(clean(stripped[2:])) + r"\b0\par" + "\n")
        elif stripped.startswith("## "):
            out.append(r"\pard\sa160\sb260\b\cf1\f0\fs28 " + esc(clean(stripped[3:])) + r"\b0\par" + "\n")
        elif stripped.startswith("### "):
            out.append(r"\pard\sa120\sb200\b\cf2\f0\fs23 " + esc(clean(stripped[4:])) + r"\b0\par" + "\n")
        elif stripped.startswith("- "):
            out.append(r"\pard\li360\fi-180\sa80\cf3\f0\fs22 \bullet\tab " + esc(clean(stripped[2:])) + r"\par" + "\n")
        elif re.match(r"^\d+\.\s+", stripped):
            m = re.match(r"^(\d+)\.\s+(.*)", stripped)
            assert m
            out.append(r"\pard\li420\fi-240\sa80\cf3\f0\fs22 " + esc(m.group(1) + ".") + r"\tab " + esc(clean(m.group(2))) + r"\par" + "\n")
        else:
            out.append(r"\pard\sa120\cf3\f0\fs22 " + esc(clean(stripped)) + r"\par" + "\n")
    flush_table()
    flush_code()
    out.append("}")
    return "".join(out)


if __name__ == "__main__":
    Path(sys.argv[2]).write_text(convert(Path(sys.argv[1]).read_text(encoding="utf-8")), encoding="utf-8")
