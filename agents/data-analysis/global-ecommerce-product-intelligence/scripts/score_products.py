#!/usr/bin/env python3
"""
Score ecommerce product candidates from a CSV file.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any


WEIGHTS = {
    "demand_strength": 20,
    "competition_access": 15,
    "review_opportunity": 15,
    "margin_space": 15,
    "differentiation_space": 15,
    "operations_simplicity": 10,
    "data_confidence": 10,
}


def parse_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    text = str(value).replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(text)
    except ValueError:
        return None


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def log_score(value: float | None, scale: float, cap: float = 100) -> float:
    if not value or value <= 0:
        return 0
    return clamp(math.log10(value + 1) / math.log10(scale + 1) * cap)


def inverse_rank_score(rank: float | None) -> float:
    if not rank or rank <= 0:
        return 0
    return clamp(100 - (math.log10(rank) / 5 * 100))


def score_record(row: dict[str, str]) -> dict[str, float]:
    rating = parse_float(row.get("rating"))
    review_count = parse_float(row.get("review_count"))
    sales_count = parse_float(row.get("sales_count"))
    bsr = parse_float(row.get("best_seller_rank"))
    monthly_sales = parse_float(row.get("monthly_sales_estimate"))
    recent_reviews = parse_float(row.get("recent_review_count"))
    trend_score = parse_float(row.get("trend_score"))
    competition_score = parse_float(row.get("competition_score"))
    margin_score = parse_float(row.get("margin_score"))
    operations_risk = parse_float(row.get("operations_risk_score"))
    differentiation_score = parse_float(row.get("differentiation_score"))

    demand_inputs = [
        log_score(review_count, 5000),
        log_score(sales_count, 20000),
        log_score(monthly_sales, 10000),
        log_score(recent_reviews, 500),
        inverse_rank_score(bsr),
    ]
    if trend_score is not None:
        demand_inputs.append(clamp(trend_score))
    demand_strength = sum(demand_inputs) / len(demand_inputs)

    if competition_score is None:
        competition_access = 50
    else:
        competition_access = clamp(competition_score)

    review_opportunity = 50
    if rating is not None and review_count:
        if rating < 4.1 and review_count >= 100:
            review_opportunity = 80
        elif 4.1 <= rating <= 4.4 and review_count >= 300:
            review_opportunity = 65
        elif rating >= 4.6:
            review_opportunity = 35

    margin_space = clamp(margin_score if margin_score is not None else 50)
    differentiation_space = clamp(differentiation_score if differentiation_score is not None else 50)
    operations_simplicity = clamp(100 - operations_risk) if operations_risk is not None else 50

    present_fields = sum(
        1
        for key in [
            "rating",
            "review_count",
            "sales_count",
            "best_seller_rank",
            "monthly_sales_estimate",
            "recent_review_count",
            "trend_score",
            "competition_score",
            "margin_score",
            "operations_risk_score",
            "differentiation_score",
        ]
        if row.get(key) not in (None, "")
    )
    data_confidence = clamp(present_fields / 11 * 100)

    return {
        "demand_strength": demand_strength,
        "competition_access": competition_access,
        "review_opportunity": review_opportunity,
        "margin_space": margin_space,
        "differentiation_space": differentiation_space,
        "operations_simplicity": operations_simplicity,
        "data_confidence": data_confidence,
    }


def total_score(scores: dict[str, float]) -> float:
    return sum(scores[key] * weight / 100 for key, weight in WEIGHTS.items())


def conclusion(score: float) -> str:
    if score >= 80:
        return "Prioritize validation"
    if score >= 65:
        return "Promising, needs more proof"
    if score >= 50:
        return "Watchlist"
    return "Do not prioritize"


def main() -> None:
    parser = argparse.ArgumentParser(description="Score ecommerce product candidates.")
    parser.add_argument("input", help="Product candidate CSV")
    parser.add_argument("-o", "--output", required=True, help="Output scored CSV")
    args = parser.parse_args()

    with Path(args.input).open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    output_rows = []
    for row in rows:
        scores = score_record(row)
        score = total_score(scores)
        output_rows.append(
            {
                **row,
                **{key: f"{value:.1f}" for key, value in scores.items()},
                "opportunity_score": f"{score:.1f}",
                "conclusion": conclusion(score),
            }
        )

    output_rows.sort(key=lambda item: float(item["opportunity_score"]), reverse=True)
    fieldnames = list(output_rows[0].keys()) if output_rows else []
    with Path(args.output).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


if __name__ == "__main__":
    main()
