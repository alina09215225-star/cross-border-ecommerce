#!/usr/bin/env python3
"""
Analyze marketplace review CSV/JSON files and produce a Markdown insight report.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


THEMES = {
    "quality_durability": [
        "quality",
        "durable",
        "durability",
        "broke",
        "broken",
        "sturdy",
        "flimsy",
        "cheap",
        "poor quality",
        "well made",
        "耐用",
        "质量",
    ],
    "material_finish": [
        "material",
        "plastic",
        "metal",
        "wood",
        "finish",
        "scratch",
        "rust",
        "paint",
        "做工",
        "材质",
    ],
    "size_fit": [
        "size",
        "fit",
        "fits",
        "small",
        "large",
        "too big",
        "too small",
        "dimension",
        "尺寸",
    ],
    "ease_of_use": [
        "easy",
        "difficult",
        "hard to",
        "convenient",
        "simple",
        "use",
        "install",
        "assembly",
        "方便",
        "安装",
    ],
    "performance": [
        "works",
        "doesn't work",
        "effective",
        "performance",
        "function",
        "效果",
        "好用",
    ],
    "shipping_packaging": [
        "shipping",
        "delivery",
        "package",
        "packaging",
        "arrived",
        "damaged",
        "物流",
        "包装",
    ],
    "customer_service": [
        "service",
        "support",
        "refund",
        "return",
        "replacement",
        "seller",
        "客服",
        "退货",
    ],
    "value_price": [
        "price",
        "value",
        "worth",
        "expensive",
        "cheap",
        "money",
        "性价比",
        "价格",
    ],
    "smell_safety": [
        "smell",
        "odor",
        "chemical",
        "safe",
        "toxic",
        "sharp",
        "气味",
        "安全",
    ],
}

STOPWORDS = {
    "the",
    "and",
    "for",
    "this",
    "that",
    "with",
    "you",
    "are",
    "was",
    "but",
    "not",
    "have",
    "has",
    "very",
    "just",
    "from",
    "they",
    "product",
    "item",
    "one",
    "use",
    "get",
    "all",
}


def read_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))
    if suffix in {".json", ".jsonl"}:
        text = path.read_text(encoding="utf-8")
        if suffix == ".jsonl":
            return [json.loads(line) for line in text.splitlines() if line.strip()]
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("reviews"), list):
            return data["reviews"]
    raise SystemExit("Unsupported input. Use CSV, JSON, or JSONL.")


def text_of(record: dict[str, Any]) -> str:
    fields = ["review_title", "title", "review_text", "text", "content", "body"]
    return " ".join(str(record.get(field, "") or "") for field in fields).strip()


def rating_of(record: dict[str, Any]) -> float | None:
    raw = record.get("rating") or record.get("stars") or record.get("score")
    if raw in (None, ""):
        return None
    match = re.search(r"\d+(?:\.\d+)?", str(raw))
    return float(match.group(0)) if match else None


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff\s'-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z][a-z'-]{2,}|\d+|[\u4e00-\u9fff]{2,}", text.lower())
    return [word for word in words if word not in STOPWORDS and len(word) > 2]


def classify_themes(text: str) -> list[str]:
    normalized = normalize_text(text)
    matched = []
    for theme, keywords in THEMES.items():
        if any(keyword.lower() in normalized for keyword in keywords):
            matched.append(theme)
    return matched or ["uncategorized"]


def is_suspicious(record: dict[str, Any], text: str) -> bool:
    rating = rating_of(record)
    normalized = normalize_text(text)
    if rating == 5 and len(normalized.split()) <= 5:
        return True
    generic = {"great product", "good product", "works great", "very good", "love it"}
    return normalized in generic


def example_snippets(records: list[dict[str, Any]], positive: bool, limit: int = 5) -> list[str]:
    snippets = []
    for record in records:
        rating = rating_of(record)
        text = text_of(record)
        if not text or rating is None:
            continue
        if positive and rating < 4:
            continue
        if not positive and rating > 2:
            continue
        snippet = re.sub(r"\s+", " ", text).strip()
        snippets.append(snippet[:260])
        if len(snippets) >= limit:
            break
    return snippets


def build_report(records: list[dict[str, Any]]) -> str:
    clean_records = [record for record in records if text_of(record)]
    ratings = [rating for record in clean_records if (rating := rating_of(record)) is not None]
    rating_counts = Counter(int(round(rating)) for rating in ratings)
    theme_counts: Counter[str] = Counter()
    theme_rating: dict[str, list[float]] = defaultdict(list)
    words: Counter[str] = Counter()
    suspicious = 0

    for record in clean_records:
        text = text_of(record)
        rating = rating_of(record)
        themes = classify_themes(text)
        for theme in themes:
            theme_counts[theme] += 1
            if rating is not None:
                theme_rating[theme].append(rating)
        words.update(tokenize(text))
        if is_suspicious(record, text):
            suspicious += 1

    lines = [
        "# Marketplace Review Analysis",
        "",
        "## Sample",
        "",
        f"- Total rows: {len(records)}",
        f"- Usable review texts: {len(clean_records)}",
        f"- Reviews with ratings: {len(ratings)}",
    ]
    if ratings:
        lines.append(f"- Average rating: {mean(ratings):.2f}")
    lines.extend(["", "## Rating Distribution", ""])
    for star in range(5, 0, -1):
        lines.append(f"- {star} star: {rating_counts.get(star, 0)}")

    lines.extend(["", "## Theme Frequency", ""])
    for theme, count in theme_counts.most_common():
        avg = theme_rating.get(theme)
        avg_text = f", avg rating {mean(avg):.2f}" if avg else ""
        lines.append(f"- {theme}: {count}{avg_text}")

    lines.extend(["", "## Frequent Terms", ""])
    for word, count in words.most_common(30):
        lines.append(f"- {word}: {count}")

    lines.extend(["", "## Positive Snippets", ""])
    for snippet in example_snippets(clean_records, positive=True):
        lines.append(f"- {snippet}")

    lines.extend(["", "## Negative Snippets", ""])
    for snippet in example_snippets(clean_records, positive=False):
        lines.append(f"- {snippet}")

    lines.extend(
        [
            "",
            "## Suspicious Review Signals",
            "",
            f"- Short generic 5-star or template-like reviews: {suspicious}",
            "",
            "## Analyst Notes",
            "",
            "- Use theme counts as a starting point, then read representative reviews before making product decisions.",
            "- Treat suspicious signals as prompts for manual inspection, not proof of review manipulation.",
            "- Translate recurring negative themes into product improvements, listing expectation management, or support fixes.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze marketplace reviews.")
    parser.add_argument("input", help="CSV, JSON, or JSONL review file")
    parser.add_argument("-o", "--output", help="Markdown output path")
    args = parser.parse_args()

    records = read_records(Path(args.input))
    report = build_report(records)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
