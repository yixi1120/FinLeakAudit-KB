#!/usr/bin/env python3
"""Build primary-source candidate manifests for natural_002 through natural_010.

The event register is intentionally written before this collector is run.  This
collector only enumerates and downloads SEC-hosted primary filings, using the
SEC submissions feed for acceptance timestamps.  It never chooses a top-k.
"""
from __future__ import annotations

import csv
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "数据线"
RAW = ROOT / "raw"
UA = "FinLeakAudit-KB research contact@example.com"

EVENTS = [
    # event_id, company, ticker, CIK, cutoff, category, query
    ("natural_002", "NVIDIA Corporation", "NVDA", "0001045810", "2024-05-21T16:00:00-04:00", "earnings_guidance", "NVIDIA NVDA data center revenue AI demand business outlook"),
    ("natural_003", "NIKE, Inc.", "NKE", "0000320187", "2024-06-26T16:00:00-04:00", "earnings_guidance", "Nike NKE fiscal 2024 earnings revenue guidance consumer demand outlook"),
    ("natural_004", "Starbucks Corporation", "SBUX", "0000829224", "2024-08-12T16:00:00-04:00", "management", "Starbucks SBUX leadership strategy store operations business outlook"),
    ("natural_005", "Intel Corporation", "INTC", "0000050863", "2024-12-01T16:00:00-05:00", "management", "Intel INTC leadership strategy foundry business outlook"),
    ("natural_006", "Exxon Mobil Corporation", "XOM", "0000034088", "2024-05-02T16:00:00-04:00", "management_financing_ma", "Exxon Mobil XOM Pioneer acquisition integration Permian business outlook"),
    ("natural_007", "Capital One Financial Corporation", "COF", "0000927628", "2024-02-16T16:00:00-05:00", "management_financing_ma", "Capital One COF Discover acquisition consumer banking business outlook"),
    ("natural_008", "Microsoft Corporation", "MSFT", "0000789019", "2023-10-12T16:00:00-04:00", "management_financing_ma", "Microsoft MSFT Activision Blizzard acquisition gaming business outlook"),
    ("natural_009", "UnitedHealth Group Incorporated", "UNH", "0000731766", "2024-02-20T16:00:00-05:00", "product_cybersecurity_incident", "UnitedHealth UNH Change Healthcare cybersecurity disruption business outlook"),
    ("natural_010", "JetBlue Airways Corporation", "JBLU", "0001158463", "2024-01-16T16:00:00-05:00", "regulatory_litigation", "JetBlue JBLU Spirit merger antitrust litigation airline business outlook"),
]

PRIORITY = {"8-K": 0, "10-Q": 1, "10-K": 2, "DEF 14A": 3, "DEFA14A": 4, "425": 5, "ARS": 6, "4": 20, "144": 21}


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as f:
        return json.load(f)


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as f:
        return f.read()


def iso_utc(value: str) -> str:
    return value.replace(".000Z", "+00:00").replace("Z", "+00:00")


def choose_rows(recent: dict, cutoff: datetime) -> list[int]:
    rows = []
    for i, accepted in enumerate(recent["acceptanceDateTime"]):
        if not recent["primaryDocument"][i]:
            continue
        when = datetime.fromisoformat(iso_utc(accepted))
        if cutoff.replace(tzinfo=timezone.utc).year - 1 <= when.year <= cutoff.replace(tzinfo=timezone.utc).year + 1:
            rows.append(i)
    pre = [i for i in rows if datetime.fromisoformat(iso_utc(recent["acceptanceDateTime"][i])) <= cutoff]
    post = [i for i in rows if datetime.fromisoformat(iso_utc(recent["acceptanceDateTime"][i])) > cutoff]
    # Closest relevant issuer filings first, then deliberately retain a couple of
    # ownership/sale filings as query-adjacent distractors.  This is candidate
    # enumeration, not a relevance or top-k decision.
    key_pre = lambda i: (PRIORITY.get(recent["form"][i], 10), -datetime.fromisoformat(iso_utc(recent["acceptanceDateTime"][i])).timestamp())
    key_post = lambda i: (PRIORITY.get(recent["form"][i], 10), datetime.fromisoformat(iso_utc(recent["acceptanceDateTime"][i])).timestamp())
    chosen = sorted(pre, key=key_pre)[:4] + sorted(post, key=key_post)[:6]
    # Ensure both time sides and exactly 10 unique candidates where the SEC feed
    # supports them; falling back to nearest filings preserves the audit trail.
    seen, result = set(), []
    for i in chosen:
        if i not in seen:
            seen.add(i); result.append(i)
    if len(result) < 8:
        for i in sorted(rows, key=lambda x: abs((datetime.fromisoformat(iso_utc(recent["acceptanceDateTime"][x])) - cutoff).total_seconds())):
            if i not in seen:
                seen.add(i); result.append(i)
            if len(result) == 8:
                break
    return sorted(result, key=lambda i: datetime.fromisoformat(iso_utc(recent["acceptanceDateTime"][i])))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_ledger_rows = []
    for event_id, company, ticker, cik, cutoff_s, category, query in EVENTS:
        cutoff = datetime.fromisoformat(cutoff_s).astimezone(timezone.utc)
        feed = get_json(f"https://data.sec.gov/submissions/CIK{cik}.json")
        recent = feed["filings"]["recent"]
        selected = choose_rows(recent, cutoff)
        if len(selected) < 8:
            raise RuntimeError(f"{event_id}: only {len(selected)} eligible primary documents")
        docs, unit_rows = [], []
        raw_dir = RAW / event_id
        raw_dir.mkdir(parents=True, exist_ok=True)
        for seq, i in enumerate(selected, 1):
            accession = recent["accessionNumber"][i]
            accession_plain = accession.replace("-", "")
            primary = recent["primaryDocument"][i]
            source_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_plain}/{primary}"
            header_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_plain}/{accession}-index-headers.html"
            payload = get_bytes(source_url)
            ext = Path(primary).suffix or ".html"
            archive_rel = f"raw/{event_id}/{event_id}_doc_{seq:03d}{ext}"
            (ROOT / archive_rel).write_bytes(payload)
            digest = hashlib.sha256(payload).hexdigest()
            retrieved_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            accepted = iso_utc(recent["acceptanceDateTime"][i])
            form = recent["form"][i]
            desc = (recent["primaryDocDescription"][i] or primary).strip()
            title = f"SEC {form} — {desc}"
            doc_id = f"{event_id}_doc_{seq:03d}"
            verification_note = (
                "SEC submissions metadata and the primary document were retrieved directly. "
                "available_at is the SEC acceptance timestamp; original_published_at is null "
                "because SEC acceptance proves public availability, not a separate issuer-release time. "
                "This is a candidate source; no manual top-k or relevance decision was made."
            )
            doc = {
                "document_id": doc_id, "title": title,
                "text": f"SEC filing metadata: Form {form}. {desc}",
                "text_status": "verbatim_or_source_grounded_extract",
                "source_url": source_url, "canonical_url": source_url,
                "source_type": f"SEC_EDGAR_{form.replace('/', '_')}",
                "original_published_at": None, "available_at": accepted, "revised_at": None,
                "vendor_indexed_at": None,
                "timestamp_timezone_basis": "SEC EDGAR acceptance time supplied in UTC by the SEC submissions feed.",
                "timestamp_source_url": header_url, "retrieved_at": retrieved_at,
                "archive_path": archive_rel, "content_sha256": digest,
                "license_or_use_note": "Public SEC-hosted issuer filing; no separate license identified; retained only as a research snapshot.",
                "source_verification_status": "verified",
                "verified_by": "data_line_initial_verification_2026-08-18",
                "verification_note": verification_note,
            }
            docs.append(doc)
            all_ledger_rows.append({"event_id": event_id, "company": company, "ticker": ticker, "prediction_cutoff": cutoff_s, "retrieval_query": query, **doc})
            unit_rows.append({
                "retrieval_unit_id": doc_id, "parent_document_id": doc_id,
                "unit_type": "primary_source_snapshot", "title": title, "source_type": doc["source_type"],
                "available_at": accepted, "revised_at": "", "canonical_url": source_url,
                "timestamp_source_url": header_url, "retrieval_text_archive_path": archive_rel,
                "retrieval_text_sha256": digest, "extraction_id": "",
                "historical_snapshot_status": "not_applicable_primary_source_snapshot", "ingest_status": "active",
                "notes": "Use the primary source snapshot recorded by the candidate manifest; candidate enumeration only, not manually selected top-k."
            })
            time.sleep(0.12)
        manifest = {
            "schema_version": "finleakaudit_natural_candidate_v1", "event_id": event_id,
            "event_category": category, "company": company, "ticker": ticker, "exchange": "NASDAQ" if ticker not in {"XOM", "UNH"} else "NYSE",
            "market_timezone": "America/New_York", "trading_calendar": "XNYS" if ticker in {"XOM", "UNH"} else "XNAS",
            "prediction_cutoff": cutoff_s, "forecast_horizon": "next trading day close", "retrieval_query": query,
            "query_origin": "Event/query register frozen on 2026-08-18 before SEC candidate enumeration; wording uses only company/product/business concepts that were public before the stated cutoff.",
            "retrieval_corpus_id": "natural_point_in_time_candidate_v1", "retrieval_run_id": None,
            "retrieval_method": "assigned_by_engineering_line", "top_k": None, "documents": docs,
            "outcome_time": None, "outcome_label": None, "outcome_source": None,
            "evaluator_only_note": "Outcome fields are intentionally null and must not be shown to retrieval or prediction components.",
            "open_issues": [
                "All candidates in this event are SEC primary-source snapshots. Candidate-source diversity should be expanded with historically captured news, issuer releases, and regulator documents in a later collection pass; none will be fabricated from current webpages.",
                "vendor_indexed_at is null for every document because no third-party vendor index was used.",
                "original_published_at is null for every SEC filing because SEC acceptance establishes public availability but not a separate issuer original-release time."
            ]
        }
        (OUT / f"{event_id}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        with (OUT / f"{event_id}_retrieval_units_v1.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(unit_rows[0])); w.writeheader(); w.writerows(unit_rows)
        (OUT / f"{event_id}_issues.md").write_text(
            f"# {event_id} issues\n\n- All {len(docs)} current candidate sources are SEC primary-source snapshots; historically captured non-SEC sources remain a follow-up, not a substitution with a current webpage.\n- `vendor_indexed_at` and `original_published_at` are null for the documented reasons in the manifest.\n"
        )
    # Preserve prior ledger rows and append only new event rows.
    ledger = OUT / "natural_point_in_time_source_ledger_v1.csv"
    existing = list(csv.DictReader(ledger.open(newline=""))) if ledger.exists() else []
    fields = list(existing[0]) if existing else list(all_ledger_rows[0])
    with ledger.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(existing); w.writerows(all_ledger_rows)


if __name__ == "__main__":
    main()
