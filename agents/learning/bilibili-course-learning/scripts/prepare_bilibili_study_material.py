#!/usr/bin/env python3
"""
Prepare a chunked markdown study packet from Bilibili transcript material.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from normalize_bilibili_subtitles import detect_and_parse


def chunk_text(text: str, chunk_size: int) -> list[str]:
    paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = paragraph if not current else current + "\n" + paragraph
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(paragraph) <= chunk_size:
                current = paragraph
            else:
                for start in range(0, len(paragraph), chunk_size):
                    part = paragraph[start : start + chunk_size]
                    if len(part) == chunk_size:
                        chunks.append(part)
                    else:
                        current = part
                if len(paragraph) % chunk_size == 0:
                    current = ""
    if current:
        chunks.append(current)
    return chunks


def build_markdown(title: str, goal: str, source: str, chunks: list[str]) -> str:
    total = len(chunks)
    lines = [
        f"# {title}",
        "",
        "## 学习目标",
        goal,
        "",
        "## 来源",
        source,
        "",
        "## 使用建议",
        "1. 先逐块提炼重点。",
        "2. 每块写一句自己的复述。",
        "3. 最后合并成总总结、回忆题和行动清单。",
        "",
        "## 分块目录",
    ]
    for index in range(total):
        lines.append(f"- 第 {index + 1}/{total} 块")
    lines.extend(["", "## 原始学习材料"])
    for index, chunk in enumerate(chunks, start=1):
        lines.extend(
            [
                "",
                f"### 第 {index}/{total} 块",
                "",
                chunk,
            ]
        )
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a chunked study markdown from transcript.")
    parser.add_argument("input", help="Path to subtitle/transcript file")
    parser.add_argument("-o", "--output", required=True, help="Output markdown file")
    parser.add_argument("--title", default="Bilibili 课程学习稿", help="Document title")
    parser.add_argument(
        "--goal",
        default="理解课程核心内容，并整理成可复习、可应用的材料。",
        help="Learning goal shown at the top of the document",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1800,
        help="Approximate character limit per chunk",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    text = detect_and_parse(input_path, keep_timestamps=False)
    chunks = chunk_text(text, args.chunk_size)
    if not chunks:
        raise SystemExit("No usable text found in input.")

    markdown = build_markdown(
        title=args.title,
        goal=args.goal,
        source=str(input_path),
        chunks=chunks,
    )
    output_path = Path(args.output)
    output_path.write_text(markdown, encoding="utf-8")
    print(
        f"Wrote {len(chunks)} chunks to {output_path} "
        f"(avg {math.ceil(len(text) / len(chunks))} chars/chunk)."
    )


if __name__ == "__main__":
    main()
