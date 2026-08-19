#!/usr/bin/env python3
"""Append missing primary event exhibits without altering existing raw files."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "数据线"

SOURCES = [
    {
        "event_id": "natural_002",
        "document_id": "natural_002_doc_019",
        "parent_document_id": "natural_002_doc_005",
        "title": "NVIDIA first-quarter fiscal 2025 earnings release",
        "source_url": "https://www.sec.gov/Archives/edgar/data/1045810/000104581024000113/q1fy25pr.htm",
        "available_at": "2024-05-22T20:21:29+00:00",
        "timestamp_source_url": "https://www.sec.gov/Archives/edgar/data/1045810/000104581024000113/0001045810-24-000113-index-headers.html",
        "source_type": "SEC_EDGAR_EXHIBIT_99_1",
        "extension": ".htm",
    },
    {
        "event_id": "natural_002",
        "document_id": "natural_002_doc_020",
        "parent_document_id": "natural_002_doc_005",
        "title": "NVIDIA first-quarter fiscal 2025 CFO commentary",
        "source_url": "https://www.sec.gov/Archives/edgar/data/1045810/000104581024000113/q1fy25cfocommentary.htm",
        "available_at": "2024-05-22T20:21:29+00:00",
        "timestamp_source_url": "https://www.sec.gov/Archives/edgar/data/1045810/000104581024000113/0001045810-24-000113-index-headers.html",
        "source_type": "SEC_EDGAR_EXHIBIT_99_2",
        "extension": ".htm",
    },
    {
        "event_id": "natural_003",
        "document_id": "natural_003_doc_019",
        "parent_document_id": "natural_003_doc_005",
        "title": "NIKE fiscal 2024 fourth-quarter and full-year results",
        "source_url": "https://www.sec.gov/Archives/edgar/data/320187/000032018724000028/q4fy24exhibit991er.htm",
        "available_at": "2024-06-27T20:16:39+00:00",
        "timestamp_source_url": "https://www.sec.gov/Archives/edgar/data/320187/000032018724000028/0000320187-24-000028-index-headers.html",
        "source_type": "SEC_EDGAR_EXHIBIT_99_1",
        "extension": ".htm",
    },
    {
        "event_id": "natural_004",
        "document_id": "natural_004_doc_019",
        "parent_document_id": "natural_004_doc_005",
        "title": "Starbucks names Brian Niccol chairman and chief executive officer",
        "source_url": "https://www.sec.gov/Archives/edgar/data/829224/000119312524200724/d848513dex991.htm",
        "available_at": "2024-08-14T21:10:59+00:00",
        "timestamp_source_url": "https://www.sec.gov/Archives/edgar/data/829224/000119312524200724/0001193125-24-200724-index-headers.html",
        "source_type": "SEC_EDGAR_EXHIBIT_99_1",
        "extension": ".htm",
    },
    {
        "event_id": "natural_005",
        "document_id": "natural_005_doc_019",
        "parent_document_id": "natural_005_doc_005",
        "title": "Intel announces retirement of CEO Pat Gelsinger",
        "source_url": "https://www.sec.gov/Archives/edgar/data/50863/000005086324000173/a12012024form8-kex991.htm",
        "available_at": "2024-12-03T00:28:44+00:00",
        "timestamp_source_url": "https://www.sec.gov/Archives/edgar/data/50863/000005086324000173/0000050863-24-000173-index-headers.html",
        "source_type": "SEC_EDGAR_EXHIBIT_99_1",
        "extension": ".htm",
    },
    {
        "event_id": "natural_006",
        "document_id": "natural_006_doc_019",
        "parent_document_id": "natural_006_doc_005",
        "title": "ExxonMobil completes acquisition of Pioneer Natural Resources",
        "source_url": "https://www.sec.gov/Archives/edgar/data/34088/000095010324006322/dp210867_ex9901.htm",
        "available_at": "2024-05-03T13:04:23+00:00",
        "timestamp_source_url": "https://www.sec.gov/Archives/edgar/data/34088/000095010324006322/0000950103-24-006322-index-headers.html",
        "source_type": "SEC_EDGAR_EXHIBIT_99_1",
        "extension": ".htm",
    },
    {
        "event_id": "natural_007",
        "document_id": "natural_007_doc_019",
        "parent_document_id": "natural_007_doc_005",
        "title": "Capital One to acquire Discover",
        "source_url": "https://www.sec.gov/Archives/edgar/data/927628/000119312524039233/d772981dex991.htm",
        "available_at": "2024-02-20T11:12:03+00:00",
        "timestamp_source_url": "https://www.sec.gov/Archives/edgar/data/927628/000119312524039233/0001193125-24-039233-index-headers.html",
        "source_type": "SEC_EDGAR_EXHIBIT_99_1",
        "extension": ".htm",
    },
    {
        "event_id": "natural_007",
        "document_id": "natural_007_doc_020",
        "parent_document_id": "natural_007_doc_005",
        "title": "Capital One and Discover transaction presentation",
        "source_url": "https://www.sec.gov/Archives/edgar/data/927628/000119312524039233/d772981dex992.htm",
        "available_at": "2024-02-20T11:12:03+00:00",
        "timestamp_source_url": "https://www.sec.gov/Archives/edgar/data/927628/000119312524039233/0001193125-24-039233-index-headers.html",
        "source_type": "SEC_EDGAR_EXHIBIT_99_2",
        "extension": ".htm",
    },
    {
        "event_id": "natural_010",
        "document_id": "natural_010_doc_019",
        "parent_document_id": "natural_010_doc_019",
        "title": "Findings of fact and conclusions of law in JetBlue-Spirit case",
        "source_url": "https://www.justice.gov/media/1380311/dl",
        "available_at": "2024-01-16T23:59:59-05:00",
        "timestamp_source_url": "https://www.justice.gov/atr/case-document/findings-fact-and-conclusions-law-v",
        "source_type": "US_DOJ_COURT_DOCUMENT",
        "extension": ".pdf",
    },
]


def request_bytes(source: dict[str, str]) -> bytes:
    if source["source_url"].startswith("https://www.sec.gov/"):
        user_agent = os.environ.get("FINLEAKAUDIT_SEC_USER_AGENT", "").strip()
        if not user_agent:
            raise RuntimeError(
                "Set FINLEAKAUDIT_SEC_USER_AGENT to a project name and real contact email"
            )
    else:
        user_agent = "FinLeakAudit-KB research source capture"
    request = urllib.request.Request(source["source_url"], headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def write_raw_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != payload:
            raise RuntimeError(f"Immutable raw collision: {path}")
        return
    path.write_bytes(payload)


def main() -> int:
    source_ledger_path = DATA / "natural_point_in_time_source_ledger_v1.csv"
    with source_ledger_path.open(encoding="utf-8", newline="") as handle:
        source_ledger = list(csv.DictReader(handle))
        source_fields = list(source_ledger[0])
    source_by_key = {
        (row["event_id"], row["document_id"]): row for row in source_ledger
    }
    additions = []

    for source in SOURCES:
        event_id = source["event_id"]
        manifest_path = DATA / f"{event_id}.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        existing_docs = {doc["document_id"]: doc for doc in manifest["documents"]}
        payload = request_bytes(source)
        archive_path = (
            f"raw/{event_id}/{source['document_id']}{source['extension']}"
        )
        write_raw_once(ROOT / archive_path, payload)
        content_hash = hashlib.sha256(payload).hexdigest()
        retrieved_at = (
            existing_docs.get(source["document_id"], {}).get("retrieved_at")
            or datetime.now(timezone.utc).isoformat(timespec="seconds")
        )
        document = {
            "document_id": source["document_id"],
            "title": source["title"],
            "text": source["title"],
            "text_status": "primary_source_title_only_retrieval_uses_archive",
            "source_url": source["source_url"],
            "canonical_url": source["source_url"],
            "source_type": source["source_type"],
            "original_published_at": None,
            "available_at": source["available_at"],
            "revised_at": None,
            "vendor_indexed_at": None,
            "timestamp_timezone_basis": (
                "SEC EDGAR acceptance timestamp in UTC."
                if source["source_type"].startswith("SEC_")
                else "Official court document exposes a filing date only; end-of-day ET is a conservative bound."
            ),
            "timestamp_source_url": source["timestamp_source_url"],
            "retrieved_at": retrieved_at,
            "archive_path": archive_path,
            "content_sha256": content_hash,
            "license_or_use_note": "Public primary-source document retained as a research snapshot.",
            "source_verification_status": "verified_primary_source",
            "verified_by": "engineering_line_source_completion_2026-08-19",
            "verification_note": (
                "Missing event body added from the primary-source filing package. "
                "No relevance score or top-k position was assigned during collection."
            ),
        }
        existing_docs[source["document_id"]] = document
        manifest["documents"] = sorted(
            existing_docs.values(), key=lambda item: item["document_id"]
        )
        if len(manifest["documents"]) > 20:
            raise ValueError(f"{event_id}: source addition exceeds 20-document protocol cap")
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        unit_path = DATA / f"{event_id}_retrieval_units_v1.csv"
        with unit_path.open(encoding="utf-8", newline="") as handle:
            units = list(csv.DictReader(handle))
            unit_fields = list(units[0])
        units_by_id = {unit["retrieval_unit_id"]: unit for unit in units}
        units_by_id[source["document_id"]] = {
            "retrieval_unit_id": source["document_id"],
            "parent_document_id": source["parent_document_id"],
            "unit_type": "primary_source_exhibit",
            "title": source["title"],
            "source_type": source["source_type"],
            "available_at": source["available_at"],
            "revised_at": "",
            "canonical_url": source["source_url"],
            "timestamp_source_url": source["timestamp_source_url"],
            "retrieval_text_archive_path": archive_path,
            "retrieval_text_sha256": content_hash,
            "extraction_id": "",
            "historical_snapshot_status": "not_applicable_primary_source_snapshot",
            "ingest_status": "active",
            "notes": "Primary event body missing from the original candidate set; no top-k position assigned.",
        }
        with unit_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=unit_fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(units_by_id[key] for key in sorted(units_by_id))

        ledger_row = {
            "event_id": event_id,
            "company": manifest["company"],
            "ticker": manifest["ticker"],
            "prediction_cutoff": manifest["prediction_cutoff"],
            "retrieval_query": manifest["retrieval_query"],
            **document,
        }
        source_by_key[(event_id, source["document_id"])] = ledger_row
        additions.append(
            {
                "event_id": event_id,
                "document_id": source["document_id"],
                "parent_document_id": source["parent_document_id"],
                "available_at": source["available_at"],
                "source_url": source["source_url"],
                "archive_path": archive_path,
                "content_sha256": content_hash,
            }
        )

    with source_ledger_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=source_fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(source_by_key[key] for key in sorted(source_by_key))

    additions_path = DATA / "natural_event_source_additions_v1.csv"
    with additions_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(additions[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(additions)
    print(f"added or verified {len(additions)} primary-source documents")
    print(f"wrote {additions_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
