#!/usr/bin/env python3
"""
Normalize subtitle-like files from Bilibili into readable plain text.

Supported input formats:
- Bilibili subtitle JSON with `body`
- plain JSON array of subtitle segments
- `.srt`
- `.vtt`
- plain text
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def format_ts(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def clean_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def dedupe_lines(lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    last = None
    for line in lines:
        normalized = clean_text(line)
        if not normalized:
            continue
        if normalized != last:
            cleaned.append(normalized)
            last = normalized
    return cleaned


def parse_bilibili_json(data: object, keep_timestamps: bool) -> str:
    if isinstance(data, dict) and isinstance(data.get("body"), list):
        items = data["body"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("Unsupported JSON subtitle structure")

    lines: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        content = clean_text(str(item.get("content", "")))
        if not content:
            continue
        if keep_timestamps:
            start = float(item.get("from", 0))
            end = float(item.get("to", 0))
            lines.append(f"[{format_ts(start)} - {format_ts(end)}] {content}")
        else:
            lines.append(content)
    return "\n".join(dedupe_lines(lines))


def parse_srt(text: str, keep_timestamps: bool) -> str:
    blocks = re.split(r"\n\s*\n", text.strip())
    lines: list[str] = []
    for block in blocks:
        parts = [line.strip() for line in block.splitlines() if line.strip()]
        if not parts:
            continue
        idx = 0
        if parts[0].isdigit():
            idx = 1
        ts = ""
        if idx < len(parts) and "-->" in parts[idx]:
            ts = parts[idx]
            idx += 1
        content = " ".join(parts[idx:])
        content = clean_text(content)
        if not content:
            continue
        if keep_timestamps and ts:
            lines.append(f"[{ts}] {content}")
        else:
            lines.append(content)
    return "\n".join(dedupe_lines(lines))


def parse_vtt(text: str, keep_timestamps: bool) -> str:
    text = re.sub(r"^WEBVTT\s*", "", text.strip(), flags=re.IGNORECASE)
    blocks = re.split(r"\n\s*\n", text)
    lines: list[str] = []
    for block in blocks:
        parts = [line.strip() for line in block.splitlines() if line.strip()]
        if not parts:
            continue
        idx = 0
        if "-->" not in parts[idx] and idx + 1 < len(parts) and "-->" in parts[idx + 1]:
            idx += 1
        ts = ""
        if idx < len(parts) and "-->" in parts[idx]:
            ts = parts[idx]
            idx += 1
        content = " ".join(parts[idx:])
        content = clean_text(content)
        if not content:
            continue
        if keep_timestamps and ts:
            lines.append(f"[{ts}] {content}")
        else:
            lines.append(content)
    return "\n".join(dedupe_lines(lines))


def detect_and_parse(path: Path, keep_timestamps: bool) -> str:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()

    if suffix == ".json":
        return parse_bilibili_json(json.loads(text), keep_timestamps)
    if suffix == ".srt":
        return parse_srt(text, keep_timestamps)
    if suffix == ".vtt":
        return parse_vtt(text, keep_timestamps)

    stripped = text.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            return parse_bilibili_json(json.loads(text), keep_timestamps)
        except Exception:
            pass
    if "WEBVTT" in stripped[:32].upper():
        return parse_vtt(text, keep_timestamps)
    if "-->" in text and re.search(r"\d{2}:\d{2}:\d{2}", text):
        return parse_srt(text, keep_timestamps)
    return clean_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Bilibili subtitles into plain text.")
    parser.add_argument("input", help="Path to subtitle file or plain text file")
    parser.add_argument("-o", "--output", help="Write output to file")
    parser.add_argument(
        "--keep-timestamps",
        action="store_true",
        help="Keep subtitle timestamps in output",
    )
    args = parser.parse_args()

    result = detect_and_parse(Path(args.input), args.keep_timestamps)
    if args.output:
        Path(args.output).write_text(result + "\n", encoding="utf-8")
    else:
        print(result)


if __name__ == "__main__":
    main()
