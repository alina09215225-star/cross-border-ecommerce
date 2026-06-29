#!/usr/bin/env python3
"""
Inspect CSV headers for product or review analysis readiness.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PRODUCT_FIELDS = {
    "product_title",
    "platform",
    "product_url",
    "price",
    "rating",
    "review_count",
}

REVIEW_FIELDS = {
    "rating",
    "review_text",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check ecommerce research input CSV fields.")
    parser.add_argument("input", help="CSV file")
    args = parser.parse_args()

    with Path(args.input).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])

    print(f"Fields found: {', '.join(sorted(fields))}")
    missing_product = sorted(PRODUCT_FIELDS - fields)
    missing_review = sorted(REVIEW_FIELDS - fields)

    if not missing_product:
        print("Product scoring: ready")
    else:
        print(f"Product scoring: missing recommended fields: {', '.join(missing_product)}")

    if not missing_review:
        print("Review analysis: ready")
    else:
        print(f"Review analysis: missing minimum fields: {', '.join(missing_review)}")


if __name__ == "__main__":
    main()
