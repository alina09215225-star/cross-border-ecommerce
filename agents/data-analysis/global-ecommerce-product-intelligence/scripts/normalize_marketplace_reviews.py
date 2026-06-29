#!/usr/bin/env python3
"""
Normalize marketplace review exports into a common CSV schema.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


TARGET_FIELDS = [
    "platform",
    "product_id",
    "product_title",
    "brand",
    "rating",
    "review_title",
    "review_text",
    "review_date",
    "variant",
    "country",
    "verified_purchase",
    "helpful_votes",
    "review_url",
]

FIELD_ALIASES = {
    "platform": ["platform", "marketplace", "site"],
    "product_id": ["product_id", "asin", "item_id", "listing_id", "sku"],
    "product_title": ["product_title", "title", "item_title", "listing_title"],
    "brand": ["brand", "seller_brand", "manufacturer"],
    "rating": ["rating", "stars", "score", "star_rating"],
    "review_title": ["review_title", "title_review", "headline", "summary"],
    "review_text": ["review_text", "text", "content", "body", "review_body", "comment"],
    "review_date": ["review_date", "date", "created_at", "review_time"],
    "variant": ["variant", "style", "color", "size", "model"],
    "country": ["country", "market", "locale", "region"],
    "verified_purchase": ["verified_purchase", "verified", "is_verified_purchase"],
    "helpful_votes": ["helpful_votes", "helpful", "likes", "upvotes"],
    "review_url": ["review_url", "url", "link"],
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
        if isinstance(data, dict):
            for key in ["reviews", "data", "items", "results"]:
                if isinstance(data.get(key), list):
                    return data[key]
    raise SystemExit("Unsupported input. Use CSV, JSON, or JSONL.")


def first_value(record: dict[str, Any], names: list[str]) -> str:
    lowered = {str(key).lower(): value for key, value in record.items()}
    for name in names:
        if name.lower() in lowered and lowered[name.lower()] not in (None, ""):
            return str(lowered[name.lower()])
    return ""


def normalize_record(record: dict[str, Any], platform_override: str | None) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for field in TARGET_FIELDS:
        normalized[field] = first_value(record, FIELD_ALIASES[field])
    if platform_override:
        normalized["platform"] = platform_override
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize marketplace review exports.")
    parser.add_argument("input", help="CSV, JSON, or JSONL review file")
    parser.add_argument("-o", "--output", required=True, help="Normalized CSV output")
    parser.add_argument("--platform", help="Force platform name, e.g. Amazon or Walmart")
    args = parser.parse_args()

    records = read_records(Path(args.input))
    normalized = [normalize_record(record, args.platform) for record in records]

    with Path(args.output).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TARGET_FIELDS)
        writer.writeheader()
        writer.writerows(normalized)


if __name__ == "__main__":
    main()
