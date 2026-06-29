#!/usr/bin/env python3
"""
Create a Markdown report skeleton from scored products and review analysis.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_top_products(path: Path, limit: int = 10) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return rows[:limit]


def build_brief(title: str, products: list[dict[str, str]], review_md: str | None) -> str:
    lines = [
        f"# {title}",
        "",
        "## Conclusion",
        "",
        "- Fill in the decision: prioritize, validate, watch, or avoid.",
        "",
        "## Product Opportunity Ranking",
        "",
        "| Rank | Product | Platform | Price | Rating | Reviews | Score | Conclusion |",
        "|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for index, row in enumerate(products, start=1):
        lines.append(
            "| {rank} | {title} | {platform} | {price} | {rating} | {reviews} | {score} | {conclusion} |".format(
                rank=index,
                title=row.get("product_title", ""),
                platform=row.get("platform", ""),
                price=row.get("price", ""),
                rating=row.get("rating", ""),
                reviews=row.get("review_count", ""),
                score=row.get("opportunity_score", ""),
                conclusion=row.get("conclusion", ""),
            )
        )

    lines.extend(
        [
            "",
            "## Market Signals",
            "",
            "- Demand:",
            "- Competition:",
            "- Price band:",
            "- Platform differences:",
            "",
            "## Review Intelligence",
            "",
        ]
    )
    if review_md:
        lines.append(review_md.strip())
    else:
        lines.append("- Add review analysis here.")

    lines.extend(
        [
            "",
            "## Opportunity Angles",
            "",
            "- Product improvement:",
            "- Listing/message improvement:",
            "- Channel opportunity:",
            "- Bundle or accessory opportunity:",
            "",
            "## Risks",
            "",
            "- Compliance:",
            "- Logistics:",
            "- Returns:",
            "- Seasonality:",
            "",
            "## Next Validation Steps",
            "",
            "1. Collect more competitor links and recent reviews.",
            "2. Validate supply cost, landed cost, and target margin.",
            "3. Test positioning with a small listing/ad/landing page experiment.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create ecommerce research report skeleton.")
    parser.add_argument("--products", help="Scored product CSV")
    parser.add_argument("--reviews", help="Review analysis Markdown")
    parser.add_argument("-o", "--output", required=True, help="Output Markdown")
    parser.add_argument("--title", default="Ecommerce Product Opportunity Report")
    args = parser.parse_args()

    products = read_top_products(Path(args.products)) if args.products else []
    review_md = Path(args.reviews).read_text(encoding="utf-8") if args.reviews else None
    report = build_brief(args.title, products, review_md)
    Path(args.output).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
