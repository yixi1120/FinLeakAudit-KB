"""Minimal FinLeakAudit operators for the pilot experiment."""

from __future__ import annotations

import re
from typing import Iterable


def temporal_availability_check(evidence_list: Iterable[dict]) -> list[dict]:
    """Mark evidence with a T+ offset as future leakage."""
    results = []
    for ev in evidence_list:
        time_str = str(ev.get("time", ""))
        status = "future_leakage" if re.match(r"^T\+\d+", time_str) else "valid"
        severity = "high" if time_str in {"T+1", "T+2"} else "medium"
        if status == "valid":
            severity = "none"
        results.append(
            {
                "evidence_id": ev["id"],
                "time": time_str,
                "temporal_status": status,
                "severity": severity,
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
    """Audit a leaky prediction and return clean evidence for revision."""
    all_evidence = case.get("clean_evidence", []) + case.get("leaked_evidence", [])
    temporal_results = temporal_availability_check(all_evidence)
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

