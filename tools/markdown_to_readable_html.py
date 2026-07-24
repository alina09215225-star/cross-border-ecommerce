#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import sys
from pathlib import Path


CSS = """
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "STHeiti", Arial, sans-serif;
  color: #14202e;
  line-height: 1.55;
  font-size: 15px;
  max-width: 820px;
  margin: 40px auto;
}
h1 { font-size: 30px; margin: 0 0 12px; color: #14202e; }
h2 { font-size: 22px; margin: 30px 0 10px; color: #2E74B5; border-bottom: 1px solid #D9E2EC; padding-bottom: 4px; }
h3 { font-size: 17px; margin: 22px 0 8px; color: #1F4D78; }
p { margin: 8px 0; }
ul, ol { margin: 8px 0 12px 24px; padding: 0; }
li { margin: 4px 0; }
table { border-collapse: collapse; width: 100%; margin: 12px 0 18px; font-size: 14px; }
th, td { border: 1px solid #D9E2EC; padding: 8px 10px; vertical-align: top; }
th { background: #E8EEF5; font-weight: 700; }
blockquote, pre {
  background: #F4F6F9;
  border: 1px solid #D9E2EC;
  padding: 10px 12px;
  margin: 12px 0;
  white-space: pre-wrap;
}
code { font-family: Menlo, Consolas, monospace; }
.meta { color: #5F6976; margin-bottom: 18px; }
"""


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\\1</strong>", text)
    return text


def markdown_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    out = ["<table>"]
    for i, row in enumerate(rows):
        tag = "th" if i == 0 else "td"
        out.append("<tr>" + "".join(f"<{tag}>{inline_md(c)}</{tag}>" for c in row) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def convert(md: str) -> str:
    lines = md.splitlines()
    out = ["<!doctype html><html><head><meta charset='utf-8'><style>", CSS, "</style></head><body>"]
    in_code = False
    code_lines: list[str] = []
    table_lines: list[str] = []
    list_mode: str | None = None

    def close_list():
        nonlocal list_mode
        if list_mode:
            out.append(f"</{list_mode}>")
            list_mode = None

    def flush_table():
        nonlocal table_lines
        if table_lines:
            close_list()
            out.append(markdown_table(table_lines))
            table_lines = []

    def flush_code():
        nonlocal code_lines
        if code_lines:
            close_list()
            out.append("<pre>" + html.escape("\n".join(code_lines)) + "</pre>")
            code_lines = []

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_table()
            if in_code:
                in_code = False
                flush_code()
            else:
                close_list()
                in_code = True
                code_lines = []
            continue
        if in_code:
            code_lines.append(line)
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines.append(stripped)
            continue
        flush_table()
        if not stripped:
            close_list()
            continue
        if stripped.startswith("# "):
            close_list()
            out.append(f"<h1>{inline_md(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            close_list()
            out.append(f"<h2>{inline_md(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            close_list()
            out.append(f"<h3>{inline_md(stripped[4:])}</h3>")
        elif stripped.startswith("- "):
            if list_mode != "ul":
                close_list()
                list_mode = "ul"
                out.append("<ul>")
            out.append(f"<li>{inline_md(stripped[2:])}</li>")
        elif re.match(r"^\\d+\\.\\s+", stripped):
            if list_mode != "ol":
                close_list()
                list_mode = "ol"
                out.append("<ol>")
            out.append(f"<li>{inline_md(re.sub(r'^\\d+\\.\\s+', '', stripped))}</li>")
        else:
            close_list()
            out.append(f"<p>{inline_md(stripped)}</p>")
    flush_table()
    flush_code()
    close_list()
    out.append("</body></html>")
    return "\n".join(out)


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    dst.write_text(convert(src.read_text(encoding="utf-8")), encoding="utf-8")
