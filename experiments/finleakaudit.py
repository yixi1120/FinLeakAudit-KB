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


def detect_semantic_leakage(
    judgments: list[dict],
    temporal_results: list[dict],
    confidence_threshold: float,
) -> dict:
    """Aggregate blinded claim-evidence judgments for future evidence."""
    future_ids = {
        item["evidence_id"]
        for item in temporal_results
        if item["temporal_status"] == "future_leakage"
    }
    evaluated = []
    leaked_pairs = []
    for judgment in judgments or []:
        evidence_id = judgment.get("evidence_id")
        if evidence_id not in future_ids:
            continue
        try:
            confidence = float(judgment.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0
        normalized = {
            **judgment,
            "semantic_dependency": str(
                judgment.get("semantic_dependency", "uncertain")
            ).strip().lower(),
            "confidence": max(0.0, min(1.0, confidence)),
        }
        evaluated.append(normalized)
        if (
            normalized["semantic_dependency"] == "yes"
            and normalized["confidence"] >= confidence_threshold
        ):
            leaked_pairs.append(normalized)

    leaked_ids = sorted(
        {item["evidence_id"] for item in leaked_pairs}
    )
    return {
        "has_leakage": bool(leaked_ids),
        "leaked_evidence_ids": leaked_ids,
        "leaked_pairs": leaked_pairs,
        "judgments": evaluated,
        "evaluated_pair_count": len(evaluated),
        "confidence_threshold": confidence_threshold,
    }


def audit_prediction(
    case: dict,
    prediction_output: dict,
    *,
    policy: str = "citation_only",
    semantic_judgments: list[dict] | None = None,
    semantic_confidence_threshold: float = 0.7,
) -> dict:
    """Audit a leaky prediction and return evidence allowed after removal."""
    if policy not in {
        "citation_only",
        "timestamp_only",
        "semantic_llm",
        "full_semantic",
    }:
        raise ValueError(f"Unsupported audit policy: {policy}")
    all_evidence = case.get("clean_evidence", []) + case.get("leaked_evidence", [])
    prediction_cutoff = case.get("prediction_cutoff") or case.get("prediction_date")
    temporal_results = temporal_availability_check(
        all_evidence,
        prediction_cutoff=prediction_cutoff,
    )
    citation_report = detect_rationale_leakage(
        prediction_output.get("rationale") or [],
        temporal_results,
    )
    citation_removed_ids = {
        evidence_id
        for leaked_claim in citation_report["leaked_claims"]
        for evidence_id in leaked_claim["leaked_evidence_ids"]
    }
    semantic_report = detect_semantic_leakage(
        semantic_judgments or [],
        temporal_results,
        semantic_confidence_threshold,
    )
    semantic_removed_ids = set(semantic_report["leaked_evidence_ids"])
    future_ids = {
        item["evidence_id"]
        for item in temporal_results
        if item["temporal_status"] == "future_leakage"
    }
    if policy == "citation_only":
        removed_ids = citation_removed_ids
    elif policy == "semantic_llm":
        removed_ids = semantic_removed_ids
    else:
        removed_ids = future_ids

    semantic_policy = policy in {"semantic_llm", "full_semantic"}
    expected_semantic_pairs = len(
        prediction_output.get("rationale") or []
    ) * len(future_ids)
    audit_complete = not semantic_policy or (
        semantic_report["evaluated_pair_count"] == expected_semantic_pairs
    )
    removal_decisions = [
        {
            "evidence_id": evidence_id,
            "removed": evidence_id in removed_ids,
            "explicit_future_citation": evidence_id in citation_removed_ids,
            "semantic_dependency_detected": evidence_id in semantic_removed_ids,
            "removal_basis": (
                "explicit_future_citation"
                if policy == "citation_only" and evidence_id in removed_ids
                else "semantic_dependency"
                if policy == "semantic_llm" and evidence_id in removed_ids
                else "post_cutoff_timestamp"
                if evidence_id in removed_ids
                else "retained_by_policy"
            ),
            "policy": policy,
        }
        for evidence_id in sorted(future_ids)
    ]

    valid_evidence = [ev for ev in all_evidence if ev["id"] not in removed_ids]
    return {
        "policy": policy,
        "leakage_detected": bool(removed_ids),
        "audit_complete": audit_complete,
        "temporal_check": temporal_results,
        "leakage_report": citation_report,
        "citation_report": citation_report,
        "semantic_report": semantic_report,
        "removal_decisions": removal_decisions,
        "removed_evidence_ids": sorted(removed_ids),
        "valid_evidence": valid_evidence,
    }
