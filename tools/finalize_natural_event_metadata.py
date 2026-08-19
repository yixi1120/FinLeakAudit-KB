#!/usr/bin/env python3
"""Apply the frozen timeline registry to manifests and source ledgers."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from natural_event_registry import EVENT_SPECS, LABEL_RULE, OUTCOME_STATUS, PRICE_FIELD


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "数据线"


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_manifests() -> list[dict[str, object]]:
    secondary_path = DATA / "natural_outcome_second_source_v1.csv"
    secondary = {}
    if secondary_path.exists():
        with secondary_path.open(encoding="utf-8", newline="") as handle:
            secondary = {row["event_id"]: row for row in csv.DictReader(handle)}
    audit_rows = []
    for event_id, spec in EVENT_SPECS.items():
        path = DATA / f"{event_id}.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        for field in (
            "company",
            "ticker",
            "exchange",
            "trading_calendar",
            "prediction_cutoff",
            "forecast_horizon",
            "event_available_at",
            "event_source",
            "event_parent_document_id",
            "event_availability_basis",
            "outcome_time",
            "outcome_label",
            "outcome_source",
            "cutoff_price",
            "outcome_price",
            "outcome_return",
        ):
            manifest[field] = spec[field]
        manifest["price_field"] = PRICE_FIELD
        manifest["return_definition"] = "outcome_close / cutoff_close - 1"
        manifest["label_rule"] = LABEL_RULE
        manifest["outcome_verification_status"] = OUTCOME_STATUS
        if event_id in secondary:
            verification = secondary[event_id]
            manifest["secondary_price_verification"] = {
                "provider": "StatMuse Money",
                "cutoff_close": float(verification["statmuse_cutoff_close"]),
                "outcome_close": float(verification["statmuse_outcome_close"]),
                "outcome_return": float(verification["statmuse_outcome_return"]),
                "outcome_label": verification["statmuse_outcome_label"],
                "direction_match": verification["direction_match"] == "True",
                "cutoff_source_url": verification["cutoff_source_url"],
                "outcome_source_url": verification["outcome_source_url"],
                "retrieved_at": verification["retrieved_at"],
            }
        manifest["timeline_validation"] = "valid_cutoff_event_outcome_order"
        manifest["timeline_validation_note"] = (
            f"cutoff={spec['prediction_cutoff']}; "
            f"event_available={spec['event_available_at']}; "
            f"outcome={spec['outcome_time']}"
        )
        manifest["evaluator_only_note"] = (
            "Outcome and price fields are evaluator-only and must never be passed to "
            "retrieval, predictor, auditor, or annotation components. Price values use "
            "two public price providers agree on direction, but their displayed "
            "values are not treated as identical or as licensed benchmark data."
        )
        path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        cutoff = datetime.fromisoformat(spec["prediction_cutoff"])
        event = datetime.fromisoformat(spec["event_available_at"])
        outcome = datetime.fromisoformat(spec["outcome_time"])
        if not cutoff < event < outcome:
            raise ValueError(f"{event_id}: invalid cutoff/event/outcome ordering")
        audit_rows.append(
            {
                "event_id": event_id,
                "ticker": spec["ticker"],
                "exchange": spec["exchange"],
                "trading_calendar": spec["trading_calendar"],
                "prediction_cutoff": spec["prediction_cutoff"],
                "event_available_at": spec["event_available_at"],
                "outcome_time": spec["outcome_time"],
                "forecast_horizon": spec["forecast_horizon"],
                "outcome_label": spec["outcome_label"],
                "outcome_return": spec["outcome_return"],
                "event_source": spec["event_source"],
                "event_parent_document_id": spec["event_parent_document_id"],
                "event_availability_basis": spec["event_availability_basis"],
                "outcome_source": spec["outcome_source"],
                "outcome_verification_status": OUTCOME_STATUS,
            }
        )
    return audit_rows


def update_query_register() -> None:
    path = DATA / "natural_event_query_register_v1.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0])
    for row in rows:
        row["prediction_cutoff"] = EVENT_SPECS[row["event_id"]]["prediction_cutoff"]
    write_csv(path, rows, fields)


def update_source_ledger() -> None:
    path = DATA / "natural_point_in_time_source_ledger_v1.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0])
    for row in rows:
        row["prediction_cutoff"] = EVENT_SPECS[row["event_id"]]["prediction_cutoff"]
    write_csv(path, rows, fields)


def update_status_unit_titles() -> None:
    path = DATA / "natural_001_retrieval_units_v1.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0])
    for row in rows:
        if row["parent_document_id"] != "natural_001_doc_012":
            continue
        sequence = row["retrieval_unit_id"].rsplit("_", 1)[-1]
        base = row["title"].removesuffix(" (first status update)")
        row["title"] = f"{base} (status update {sequence}/13)"
    write_csv(path, rows, fields)


def main() -> int:
    audit_rows = update_manifests()
    update_query_register()
    update_source_ledger()
    update_status_unit_titles()
    audit_path = DATA / "natural_event_timeline_audit_v1.csv"
    write_csv(audit_path, audit_rows, list(audit_rows[0]))
    print(f"updated {len(audit_rows)} event manifests")
    print(f"wrote {audit_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
