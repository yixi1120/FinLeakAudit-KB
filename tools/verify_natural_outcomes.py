#!/usr/bin/env python3
"""Cross-check frozen outcome directions against StatMuse closing-price pages."""

from __future__ import annotations

import csv
import html
import re
import urllib.request
from datetime import datetime
from pathlib import Path

from natural_event_registry import EVENT_SPECS


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "数据线" / "natural_outcome_second_source_v1.csv"
DESCRIPTION_PATTERN = re.compile(
    r'<meta name="description" content="([^"]+)"', re.IGNORECASE
)
PRICE_PATTERN = re.compile(r"closing price .*? was \$([0-9,]+(?:\.[0-9]+)?)", re.IGNORECASE)


def statmuse_url(ticker: str, value: str) -> str:
    date = datetime.fromisoformat(value).date()
    date_slug = date.strftime("%B-%d-%Y").replace("-0", "-").lower()
    return f"https://www.statmuse.com/money/ask/{ticker}-stock-price-on-{date_slug}"


def fetch_close(url: str) -> float:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        page = response.read().decode("utf-8", errors="ignore")
    description_match = DESCRIPTION_PATTERN.search(page)
    if not description_match:
        raise ValueError(f"No description metadata found at {url}")
    description = html.unescape(description_match.group(1))
    price_match = PRICE_PATTERN.search(description)
    if not price_match:
        raise ValueError(f"No closing price found in metadata at {url}")
    return float(price_match.group(1).replace(",", ""))


def main() -> int:
    existing_retrieved = {}
    if OUTPUT.exists():
        with OUTPUT.open(encoding="utf-8", newline="") as handle:
            existing_retrieved = {
                row["event_id"]: row["retrieved_at"] for row in csv.DictReader(handle)
            }
    rows = []
    mismatches = []
    for event_id, spec in EVENT_SPECS.items():
        cutoff_url = statmuse_url(spec["ticker"], spec["prediction_cutoff"])
        outcome_url = statmuse_url(spec["ticker"], spec["outcome_time"])
        cutoff_close = fetch_close(cutoff_url)
        outcome_close = fetch_close(outcome_url)
        outcome_return = outcome_close / cutoff_close - 1
        label = "UP" if outcome_return > 0 else "DOWN" if outcome_return < 0 else "NEUTRAL"
        direction_match = label == spec["outcome_label"]
        if not direction_match:
            mismatches.append(event_id)
        rows.append(
            {
                "event_id": event_id,
                "ticker": spec["ticker"],
                "cutoff_date": datetime.fromisoformat(spec["prediction_cutoff"]).date(),
                "outcome_date": datetime.fromisoformat(spec["outcome_time"]).date(),
                "statmuse_cutoff_close": cutoff_close,
                "statmuse_outcome_close": outcome_close,
                "statmuse_outcome_return": round(outcome_return, 8),
                "statmuse_outcome_label": label,
                "registry_outcome_label": spec["outcome_label"],
                "direction_match": direction_match,
                "cutoff_source_url": cutoff_url,
                "outcome_source_url": outcome_url,
                "retrieved_at": existing_retrieved.get(event_id, "2026-08-19"),
            }
        )
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUTPUT}: direction matched in {len(rows) - len(mismatches)}/{len(rows)}")
    if mismatches:
        print(f"direction mismatches: {', '.join(mismatches)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
