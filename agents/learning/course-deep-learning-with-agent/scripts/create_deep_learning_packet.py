#!/usr/bin/env python3
"""
Create a deep-learning markdown packet from raw course text.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def chunk_text(text: str, chunk_size: int) -> list[str]:
    paragraphs = [line.strip() for line in text.splitlines() if line.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = paragraph if not current else current + "\n" + paragraph
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = paragraph
    if current:
        chunks.append(current)
    return chunks


def build_packet(title: str, goal: str, source: str, chunks: list[str]) -> str:
    lines = [
        f"# {title}",
        "",
        "## 学习目标",
        goal,
        "",
        "## 使用说明",
        "按“结论-原理-证据-边界-迁移-检验”六层来学习，不要直接跳到行动方案。",
        "",
        "## 源材料",
        source,
        "",
        "## 建议流程",
        "1. 先识别课程在回答什么问题。",
        "2. 从每一块里提炼主判断和证据。",
        "3. 标出边界、反例和容易误解的地方。",
        "4. 最后迁移到自己的业务场景，再给行动方案。",
        "",
        "## 深学记录模板",
        "",
        "### 这门课到底在回答什么问题",
        "",
        "### 一句话主判断",
        "",
        "### 为什么会得出这个判断",
        "",
        "### 证据链",
        "",
        "### 边界与反例",
        "",
        "### 放到我的场景里意味着什么",
        "",
        "### 我如何检验自己学会了",
        "",
        "## 原始材料分块",
    ]
    total = len(chunks)
    for idx, chunk in enumerate(chunks, start=1):
        lines.extend(["", f"### 第 {idx}/{total} 块", "", chunk])
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create deep-learning packet from course text.")
    parser.add_argument("input", help="Transcript, notes, or markdown file")
    parser.add_argument("-o", "--output", required=True, help="Output markdown path")
    parser.add_argument("--title", default="课程深度学习工作包")
    parser.add_argument(
        "--goal",
        default="真正学懂课程的判断逻辑、证据链、边界条件，并迁移到自己的真实场景。",
    )
    parser.add_argument("--chunk-size", type=int, default=2200)
    args = parser.parse_args()

    input_path = Path(args.input)
    text = input_path.read_text(encoding="utf-8")
    chunks = chunk_text(text, args.chunk_size)
    if not chunks:
        raise SystemExit("No usable text found.")

    packet = build_packet(args.title, args.goal, str(input_path), chunks)
    Path(args.output).write_text(packet, encoding="utf-8")
    print(f"Wrote deep-learning packet to {args.output} with {len(chunks)} chunks.")


if __name__ == "__main__":
    main()
