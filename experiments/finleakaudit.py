"""Minimal FinLeakAudit operators for the pilot experiment."""

from __future__ import annotations

from datetime import datetime
import re
from typing import Iterable


def parse_timestamp(value: object) -> datetime | None:
    """Parse an aware ISO-8601 timestamp, returning None for invalid values."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def temporal_availability_check(
    evidence_list: Iterable[dict],
    prediction_cutoff: object = None,
) -> list[dict]:
    """Classify evidence using absolute availability, with a legacy fallback."""
    cutoff = parse_timestamp(prediction_cutoff)
    results = []
    for ev in evidence_list:
        time_str = str(ev.get("time", ""))
        available_at = ev.get("available_at")
        available = parse_timestamp(available_at)

        if available_at:
            if cutoff is None or available is None:
                status = "unknown"
                severity = "unknown"
                basis = "invalid_or_missing_absolute_timestamp"
            else:
                status = "future_leakage" if available > cutoff else "valid"
                severity = "high" if status == "future_leakage" else "none"
                basis = "absolute_timestamp"
        else:
            status = "future_leakage" if re.match(r"^T\+\d+", time_str) else "valid"
            severity = "high" if status == "future_leakage" else "none"
            basis = "relative_time_fallback"

        results.append(
            {
                "evidence_id": ev["id"],
                "time": time_str,
                "available_at": available_at,
                "prediction_cutoff": prediction_cutoff,
                "temporal_status": status,
                "severity": severity,
                "availability_basis": basis,
            }
        )
    return results


def detect_rationale_leakage(rationale: list[dict], temporal_results: list[dict]) -> dict:
    """Find claims that explicitly cite future evidence IDs."""
    future_ids = {
        item["evidence_id"]
        for item in temporal_results
        if item["temporal_status"] == "future_leakage"
    }

    leaked_claims = []
    for claim in rationale or []:
        cited_ids = set(claim.get("evidence_ids") or [])
        leaked = sorted(cited_ids & future_ids)
        if leaked:
            leaked_claims.append(
                {
                    "claim": claim.get("claim", ""),
                    "leaked_evidence_ids": leaked,
                    "all_cited_ids": sorted(cited_ids),
                }
            )

    return {
        "has_leakage": bool(leaked_claims),
        "leaked_claims": leaked_claims,
        "leakage_count": len(leaked_claims),
        "total_claims": len(rationale or []),
    }


def audit_prediction(case: dict, prediction_output: dict) -> dict:
    """Audit a leaky prediction and return evidence allowed after removal."""
    all_evidence = case.get("clean_evidence", []) + case.get("leaked_evidence", [])
    prediction_cutoff = case.get("prediction_cutoff") or case.get("prediction_date")
    temporal_results = temporal_availability_check(
        all_evidence,
        prediction_cutoff=prediction_cutoff,
    )
    leakage_report = detect_rationale_leakage(
        prediction_output.get("rationale") or [],
        temporal_results,
    )

    removed_ids = set()
    for leaked_claim in leakage_report["leaked_claims"]:
        removed_ids.update(leaked_claim["leaked_evidence_ids"])

    valid_evidence = [ev for ev in all_evidence if ev["id"] not in removed_ids]
    return {
        "leakage_detected": leakage_report["has_leakage"],
        "temporal_check": temporal_results,
        "leakage_report": leakage_report,
        "removed_evidence_ids": sorted(removed_ids),
        "valid_evidence": valid_evidence,
    }
