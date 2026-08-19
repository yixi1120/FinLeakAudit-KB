#!/usr/bin/env python3
"""Validate natural manifests, timelines, immutable files, and retrieval units."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

from natural_event_registry import EVENT_SPECS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "数据线"
KNOWN_STATUSES = {
    "active",
    "blocked_historical_snapshot_required",
    "superseded",
}
FORBIDDEN_CURRENT_WEB_SNAPSHOTS = {
    "raw/natural_001/natural_001_doc_015.html",
    "raw/natural_001/natural_001_doc_016.html",
    "raw/natural_001/natural_001_doc_018.html",
    "raw/natural_001/natural_001_doc_019.html",
    "raw/natural_001/natural_001_doc_020.html",
    "raw/natural_001/natural_001_doc_021.html",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_manifest(
    manifest: dict[str, object], errors: list[str]
) -> tuple[datetime, datetime]:
    event_id = str(manifest["event_id"])
    spec = EVENT_SPECS[event_id]
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
        "outcome_time",
        "outcome_label",
        "outcome_source",
    ):
        if manifest.get(field) != spec[field]:
            errors.append(
                f"{event_id}: manifest {field} differs from frozen event registry"
            )

    cutoff = datetime.fromisoformat(str(manifest["prediction_cutoff"]))
    event_time = datetime.fromisoformat(str(manifest["event_available_at"]))
    outcome = datetime.fromisoformat(str(manifest["outcome_time"]))
    if not cutoff < event_time < outcome:
        errors.append(f"{event_id}: expected cutoff < event_available_at < outcome")

    calculated_return = float(manifest["outcome_price"]) / float(
        manifest["cutoff_price"]
    ) - 1
    if abs(calculated_return - float(manifest["outcome_return"])) > 1e-6:
        errors.append(f"{event_id}: outcome_return does not match recorded prices")
    expected_label = (
        "UP" if calculated_return > 0 else "DOWN" if calculated_return < 0 else "NEUTRAL"
    )
    if manifest["outcome_label"] != expected_label:
        errors.append(f"{event_id}: outcome_label does not match return sign")

    documents = list(manifest.get("documents") or [])
    if not 8 <= len(documents) <= 20:
        errors.append(f"{event_id}: document count outside protocol range 8-20")
    document_ids = [str(item["document_id"]) for item in documents]
    if len(document_ids) != len(set(document_ids)):
        errors.append(f"{event_id}: duplicate document IDs")
    return cutoff, outcome


def main() -> int:
    errors: list[str] = []
    active: list[dict[str, str]] = []
    coverage: dict[str, dict[str, int]] = {}
    manifests = sorted(DATA.glob("natural_0[0-9][0-9].json"))
    if len(manifests) != 10:
        errors.append(f"expected exactly 10 event manifests, found {len(manifests)}")

    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        event_id = str(manifest["event_id"])
        if event_id not in EVENT_SPECS:
            errors.append(f"{event_id}: missing from frozen event registry")
            continue
        cutoff, outcome = validate_manifest(manifest, errors)
        documents = {
            str(item["document_id"]): item for item in manifest.get("documents") or []
        }

        units_path = DATA / f"{event_id}_retrieval_units_v1.csv"
        if not units_path.exists():
            errors.append(f"{event_id}: missing retrieval-unit ledger")
            continue
        with units_path.open(encoding="utf-8", newline="") as handle:
            units = list(csv.DictReader(handle))
        unit_ids = [unit["retrieval_unit_id"] for unit in units]
        if len(unit_ids) != len(set(unit_ids)):
            errors.append(f"{event_id}: duplicate retrieval unit IDs")

        pre_cutoff = 0
        post_cutoff = 0
        event_source_is_active = False
        event_parent_is_active = False
        for unit in units:
            status = unit["ingest_status"]
            if status not in KNOWN_STATUSES:
                errors.append(
                    f"{unit['retrieval_unit_id']}: unknown ingest_status {status!r}"
                )
                continue
            if status != "active":
                continue
            unit_id = unit["retrieval_unit_id"]
            if unit["parent_document_id"] not in documents:
                errors.append(f"{unit_id}: parent document missing from manifest")
            if unit["retrieval_text_archive_path"] in FORBIDDEN_CURRENT_WEB_SNAPSHOTS:
                errors.append(f"{unit_id}: current full-page web snapshot is forbidden")
                continue
            if not unit["available_at"]:
                errors.append(f"{unit_id}: active unit has null available_at")
                continue
            available = datetime.fromisoformat(unit["available_at"])
            if available > outcome:
                # Post-outcome distractors are valid corpus candidates, but they
                # cannot appear in an outcome-bounded retrieval run.
                pass
            if available <= cutoff:
                pre_cutoff += 1
            else:
                post_cutoff += 1

            source_path = ROOT / unit["retrieval_text_archive_path"]
            if not source_path.exists():
                errors.append(f"{unit_id}: missing retrieval path {source_path}")
                continue
            if digest(source_path) != unit["retrieval_text_sha256"]:
                errors.append(f"{unit_id}: retrieval source hash mismatch")
            if manifest["event_source"] in {
                unit["canonical_url"],
                unit["timestamp_source_url"],
            }:
                event_source_is_active = True
            if unit["parent_document_id"] == manifest["event_parent_document_id"]:
                event_parent_is_active = True
            active.append(
                {
                    "event_id": event_id,
                    "retrieval_unit_id": unit_id,
                    "parent_document_id": unit["parent_document_id"],
                    "available_at": unit["available_at"],
                    "path": unit["retrieval_text_archive_path"],
                    "sha256": unit["retrieval_text_sha256"],
                }
            )

        if pre_cutoff == 0 or post_cutoff == 0:
            errors.append(f"{event_id}: active corpus must contain pre- and post-cutoff units")
        if not event_source_is_active:
            errors.append(f"{event_id}: frozen primary event source is not an active unit")
        if not event_parent_is_active:
            errors.append(f"{event_id}: event parent has no active retrieval unit")
        coverage[event_id] = {
            "active_pre_cutoff_units": pre_cutoff,
            "active_post_cutoff_units": post_cutoff,
        }

    categories = {
        json.loads(path.read_text(encoding="utf-8")).get("event_category")
        for path in manifests
    }
    required = {
        "earnings_guidance",
        "regulatory_litigation",
        "product_cybersecurity_incident",
    }
    if not required.issubset(categories) or not (
        {"management", "management_financing_ma"} & categories
    ):
        errors.append("event categories do not cover protocol minimum")

    report = {
        "validator": "validate_natural_retrieval_corpus.py",
        "event_manifests": len(manifests),
        "active_retrieval_units": len(active),
        "timeline_and_source_coverage": coverage,
        "errors": errors,
        "active_units": active,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
