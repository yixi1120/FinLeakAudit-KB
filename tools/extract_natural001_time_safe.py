"""Build append-only, time-scoped retrieval texts for natural_001 web sources.

The original downloaded HTML remains immutable under raw/natural_001/.  This
script adds plain-text body extracts and a separate extraction ledger.  It does
not overwrite an existing raw extract unless its bytes are identical.
"""

import csv
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from lxml import html


ROOT = Path.cwd()
RAW = ROOT / "raw" / "natural_001"
EXTRACTED = RAW / "extracted"
OUT = ROOT / "数据线"
MANIFEST = OUT / "natural_001.json"
SOURCE_LEDGER = OUT / "natural_point_in_time_source_ledger_v1.csv"
EXTRACTION_LEDGER = OUT / "natural_001_extraction_ledger_v1.csv"
RETRIEVAL_UNITS = OUT / "natural_001_retrieval_units_v1.csv"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_text(node) -> str:
    """Keep only visible text in a selected editorial/status-content subtree."""
    for unwanted in node.xpath(".//script|.//style|.//noscript"):
        unwanted.drop_tree()
    return re.sub(r"\s+", " ", " ".join(node.xpath(".//text()"))).strip()


def write_raw_add_only(path: Path, text: str) -> str:
    data = (text.strip() + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError(f"refusing to modify immutable raw extract: {path}")
    if not path.exists():
        path.write_bytes(data)
    return sha256(data)


def snapshot_meta(path: Path):
    data = path.read_bytes()
    return f"raw/natural_001/{path.name}", sha256(data)


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {doc["document_id"]: doc for doc in manifest["documents"]}
    extraction_run_at = datetime.now().astimezone().isoformat(timespec="seconds")
    # `extracted_at` is provenance of the first successful extraction, not the
    # time this deterministic manifest generator was last rerun. Preserve it
    # for existing extraction IDs so routine validation does not create drift.
    existing_extracted_at = {}
    if EXTRACTION_LEDGER.exists():
        with EXTRACTION_LEDGER.open(newline="", encoding="utf-8") as f:
            for prior in csv.DictReader(f):
                if prior.get("extraction_id") and prior.get("extracted_at"):
                    existing_extracted_at[prior["extraction_id"]] = prior["extracted_at"]

    def stable_extracted_at(extraction_id: str) -> str:
        return existing_extracted_at.get(extraction_id, extraction_run_at)

    rows = []

    # The XPath targets deliberately exclude global navigation, related links,
    # newsletter modules, ads, footer content, and all scripts/styles.
    body_specs = {
        "natural_001_doc_015": (
            "natural_001_doc_015.html",
            '//*[contains(concat(" ", normalize-space(@class), " "), " wp-block-post-content ")]',
            "lxml HTML parser; selected WordPress wp-block-post-content editorial body; removed script/style/noscript; collapsed whitespace.",
        ),
        "natural_001_doc_016": (
            "natural_001_doc_016.html",
            '//*[contains(concat(" ", normalize-space(@class), " "), " text--blog-content ")]',
            "lxml HTML parser; selected CrowdStrike text--blog-content editorial body; removed script/style/noscript; collapsed whitespace.",
        ),
        "natural_001_doc_018": (
            "natural_001_doc_018.html",
            '//*[contains(concat(" ", normalize-space(@class), " "), " text--blog-content ")]',
            "lxml HTML parser; selected CrowdStrike text--blog-content editorial body; removed script/style/noscript; collapsed whitespace.",
        ),
        "natural_001_doc_019": (
            "natural_001_doc_019.html",
            '//*[contains(concat(" ", normalize-space(@class), " "), " text--blog-content ")]',
            "lxml HTML parser; selected CrowdStrike text--blog-content editorial body; removed script/style/noscript; collapsed whitespace.",
        ),
        "natural_001_doc_020": (
            "natural_001_doc_020.html",
            '//*[contains(concat(" ", normalize-space(@class), " "), " text--blog-content ")]',
            "lxml HTML parser; selected CrowdStrike text--blog-content editorial body; removed script/style/noscript; collapsed whitespace.",
        ),
        "natural_001_doc_021": (
            "natural_001_doc_021.html",
            '//section[@id="content-body"]/p[not(descendant::i)][not(starts-with(normalize-space(.), "UPDATE:"))]',
            "lxml HTML parser; selected TechTarget #content-body direct editorial paragraphs; excluded ad/related-content sections, author/update byline, scripts/styles, and the later UPDATE paragraph; collapsed whitespace.",
        ),
    }

    for document_id, (filename, xpath, method) in body_specs.items():
        source = RAW / filename
        tree = html.parse(str(source))
        nodes = tree.xpath(xpath)
        if not nodes:
            raise RuntimeError(f"expected an editorial body for {document_id}, found none")
        text = "\n\n".join(clean_text(node) for node in nodes if clean_text(node))
        if not text:
            raise RuntimeError(f"empty editorial body for {document_id}")
        # v2 specifically replaces the v1 TechTarget extract, whose selected
        # container included a related-articles module and later UPDATE text.
        suffix = "_body_v2.txt" if document_id == "natural_001_doc_021" else "_body.txt"
        extract_rel = f"raw/natural_001/extracted/{document_id}{suffix}"
        extract_hash = write_raw_add_only(ROOT / extract_rel, text)
        source_rel, source_hash = snapshot_meta(source)
        doc = by_id[document_id]
        doc["archive_path"] = extract_rel
        doc["content_sha256"] = extract_hash
        doc["retrieval_text_status"] = "editorial_body_extract_current_snapshot"
        time_note = (
            " content_available_at is null because the primary page exposes only a calendar date without a precise time and timezone."
            if doc["available_at"] is None else ""
        )
        extraction_id = f"{document_id}_body_v2" if document_id == "natural_001_doc_021" else f"{document_id}_body_v1"
        rows.append({
            "extraction_id": extraction_id,
            "parent_document_id": document_id,
            "unit_type": "editorial_body",
            "content_available_at": doc["available_at"],
            "content_revised_at": doc["revised_at"],
            "historical_snapshot_url": None,
            "historical_snapshot_status": "not_verified_in_this_pass",
            "source_snapshot_archive_path": source_rel,
            "source_snapshot_sha256": source_hash,
            "extracted_text_archive_path": extract_rel,
            "extracted_content_sha256": extract_hash,
            "extraction_method": method,
            "extracted_at": stable_extracted_at(extraction_id),
            "notes": "The source HTML was downloaded in 2026. This is a body-only extract, not a verified historical-page snapshot; do not use it for an as-of-time claim requiring a historical capture." + time_note,
        })

    # Correct the two explicit metadata defects reported by the audit.
    tc = by_id["natural_001_doc_015"]
    tc["revised_at"] = "2024-07-20T06:23:00+00:00"
    tc["verification_note"] = (
        "Post-cutoff. datePublished and dateModified were directly read from the page's NewsArticle JSON-LD. "
        "The retrieval text is a body-only extract; historical archive availability was not verified. "
        "vendor_indexed_at is null because no third-party vendor copy or vendor-index timestamp was used."
    )
    tt = by_id["natural_001_doc_021"]
    canonical = "https://www.techtarget.com/cybersecurity/news/366596579/CrowdStrike-Content-validation-bug-led-to-global-outage"
    tt["source_url"] = canonical
    tt["canonical_url"] = canonical
    tt["timestamp_source_url"] = canonical
    tt["original_published_at"] = "2024-07-24T11:11:00+00:00"
    tt["available_at"] = "2024-07-24T11:11:00+00:00"
    tt["timestamp_timezone_basis"] = "Source HTML datePublished = 2024-07-24T11:11Z; UTC explicit."
    tt["revised_at"] = None
    tt["source_verification_status"] = "verified"
    tt["verification_note"] = (
        "datePublished was directly read from source HTML as 2024-07-24T11:11Z. The page visibly says it was updated on 2024-08-06, "
        "but gives no exact revision time, so revised_at is null rather than inferred. "
        "The canonical URL was directly read from the source HTML. The retrieval text is a body-only extract; "
        "historical archive availability was not verified. vendor_indexed_at is null because no third-party vendor copy or vendor-index timestamp was used."
    )
    # Body rows were created before these two metadata corrections.  Refresh
    # their time fields from the canonical manifest so the extraction ledger
    # is the authoritative per-extract timing record as well.
    for row in rows:
        doc = by_id[row["parent_document_id"]]
        row["content_available_at"] = doc["available_at"]
        row["content_revised_at"] = doc["revised_at"]
        null_reason = " content_available_at is null because the primary page exposes only a calendar date without a precise time and timezone."
        if doc["available_at"] is None and null_reason not in row["notes"]:
            row["notes"] += null_reason
        if doc["available_at"] is not None:
            row["notes"] = row["notes"].replace(null_reason, "")
    # The first TechTarget extraction was already added to immutable raw/.
    # Preserve its provenance explicitly, but mark it superseded: it included
    # a related-content module and a later UPDATE paragraph and is never the
    # retrieval path in the manifest.
    legacy_tt = ROOT / "raw/natural_001/extracted/natural_001_doc_021_body.txt"
    if legacy_tt.exists():
        legacy_time = datetime.fromtimestamp(legacy_tt.stat().st_mtime).astimezone().isoformat(timespec="seconds")
        rows.append({
            "extraction_id": "natural_001_doc_021_body_v1_superseded",
            "parent_document_id": "natural_001_doc_021",
            "unit_type": "superseded_editorial_body",
            "content_available_at": tt["available_at"],
            "content_revised_at": None,
            "historical_snapshot_url": None,
            "historical_snapshot_status": "not_verified_in_this_pass",
            "source_snapshot_archive_path": "raw/natural_001/natural_001_doc_021.html",
            "source_snapshot_sha256": sha256((RAW / "natural_001_doc_021.html").read_bytes()),
            "extracted_text_archive_path": "raw/natural_001/extracted/natural_001_doc_021_body.txt",
            "extracted_content_sha256": sha256(legacy_tt.read_bytes()),
            "extraction_method": "lxml HTML parser; selected TechTarget #content-body editorial section; removed script/style/noscript; collapsed whitespace.",
            "extracted_at": legacy_time,
            "notes": "Superseded and excluded from retrieval because it included a related-content module and a later UPDATE paragraph. Retained only because raw/ is append-only.",
        })

    # The current Google page is an end-state history.  Each timestamped update
    # becomes an independent retrieval unit; the main document points only to
    # the earliest update instead of exposing the final aggregate page.
    google_source = RAW / "natural_001_doc_012.html"
    tree = html.parse(str(google_source))
    update_rows = tree.xpath('//table[contains(concat(" ", normalize-space(@class), " "), " status-updates ")]//tbody/tr')
    if len(update_rows) != 13:
        raise RuntimeError(f"expected 13 Google status updates, found {len(update_rows)}")
    source_rel, source_hash = snapshot_meta(google_source)
    updates = []
    for row in update_rows:
        date = clean_text(row.xpath('./th[contains(@class, "date")]')[0])
        clock = clean_text(row.xpath('./td[contains(@class, "time")]')[0])
        description = clean_text(row.xpath('./td[contains(@class, "description")]')[0])
        updates.append((date, clock, description))
    # Source is newest-first. The explicit sequence is oldest-first.
    for sequence, (date, clock, description) in enumerate(reversed(updates), 1):
        # All listed dates are 19 Jul except the first, which is 18 Jul.
        day = "2024-07-18" if date.startswith("18 ") else "2024-07-19"
        hour, minute = clock.split()[0].split(":")
        available_at = f"{day}T{hour}:{minute}:00-07:00"
        unit_id = f"natural_001_doc_012_update_{sequence:02d}"
        extract_rel = f"raw/natural_001/extracted/{unit_id}.txt"
        extract_hash = write_raw_add_only(ROOT / extract_rel, description)
        rows.append({
            "extraction_id": unit_id,
            "parent_document_id": "natural_001_doc_012",
            "unit_type": "status_update",
            "content_available_at": available_at,
            "content_revised_at": None,
            "historical_snapshot_url": None,
            "historical_snapshot_status": "status_history_reconstructed_from_current_page",
            "source_snapshot_archive_path": source_rel,
            "source_snapshot_sha256": source_hash,
            "extracted_text_archive_path": extract_rel,
            "extracted_content_sha256": extract_hash,
            "extraction_method": "lxml HTML parser; selected one row from table.status-updates (date, time, description); removed script/style/noscript; collapsed whitespace.",
            "extracted_at": stable_extracted_at(unit_id),
            "notes": "Timestamp is displayed by Google in US/Pacific (PDT on this date). This unit contains only this update, never the final aggregate incident page.",
        })
    first = rows[-13]
    google = by_id["natural_001_doc_012"]
    google["title"] = "Google Cloud Service Health — Windows VMs using CrowdStrike are crashing (first status update)"
    google["text"] = (ROOT / first["extracted_text_archive_path"]).read_text(encoding="utf-8").strip()
    google["original_published_at"] = first["content_available_at"]
    google["available_at"] = first["content_available_at"]
    google["revised_at"] = None
    google["timestamp_timezone_basis"] = "Google incident history displays all times as US/Pacific; PDT (-07:00) applies on 2024-07-18/19."
    google["archive_path"] = first["extracted_text_archive_path"]
    google["content_sha256"] = first["extracted_content_sha256"]
    google["retrieval_text_status"] = "first_status_update_only; all 13 separately timestamped units are in natural_001_extraction_ledger_v1.csv"
    google["verification_note"] = (
        "The first status update is 2024-07-18 23:48 PDT, directly displayed in the incident history. "
        "The final aggregate incident page is retained only as an immutable source snapshot; its 13 updates are separate extraction-ledger units. "
        "vendor_indexed_at is null because no third-party vendor copy or vendor-index timestamp was used."
    )

    manifest["open_issues"] = list(dict.fromkeys(
        issue for issue in manifest["open_issues"] if "Engineering must use each" not in issue
    ))
    required_open_issues = [
        "Web retrieval text is body-only and recorded in natural_001_extraction_ledger_v1.csv. No historical archive snapshot was verified in this pass for documents 015, 016, 018, 019, 020, or 021; their 2026-page body extracts must not support an as-of-time content claim without a later historical-capture verification.",
        "Google document 012 is represented by 13 separately timestamped status-update extraction units. The primary manifest points only to the earliest update (2024-07-18 23:48 PDT), never to the final aggregate status page.",
    ]
    for issue in required_open_issues:
        if issue not in manifest["open_issues"]:
            manifest["open_issues"].append(issue)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Keep the protocol's source-ledger schema intact; it references the
    # retrieval text now used by engineering. The extraction ledger supplies
    # the additional method/version/hash fields without silently changing the
    # template columns.
    with SOURCE_LEDGER.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        other_event_rows = [row for row in reader if row["event_id"] != "natural_001"]
    with SOURCE_LEDGER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(other_event_rows)
        for doc in manifest["documents"]:
            writer.writerow(
                {
                    key: manifest.get(key) if key in manifest else doc.get(key)
                    for key in fieldnames
                }
            )

    extraction_fields = [
        "extraction_id", "parent_document_id", "unit_type", "content_available_at", "content_revised_at",
        "historical_snapshot_url", "historical_snapshot_status", "source_snapshot_archive_path", "source_snapshot_sha256",
        "extracted_text_archive_path", "extracted_content_sha256", "extraction_method", "extracted_at", "notes",
    ]
    with EXTRACTION_LEDGER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=extraction_fields)
        writer.writeheader()
        writer.writerows(rows)

    # One loader-facing list resolves the mixed grain between source documents
    # and content versions.  Engineering must index exactly these active units:
    # primary SEC/PDF snapshots, editorial-body extracts, and each individual
    # Google status update.  It intentionally excludes the superseded TT v1
    # extract and every full-page 2026 web snapshot.
    active_extracts = [r for r in rows if r["unit_type"] in {"editorial_body", "status_update"}]
    extract_by_parent = {}
    for row in active_extracts:
        extract_by_parent.setdefault(row["parent_document_id"], []).append(row)
    unit_fields = [
        "retrieval_unit_id", "parent_document_id", "unit_type", "title", "source_type", "available_at", "revised_at",
        "canonical_url", "timestamp_source_url", "retrieval_text_archive_path", "retrieval_text_sha256", "extraction_id",
        "historical_snapshot_status", "ingest_status", "notes",
    ]
    unit_rows = []
    for doc in manifest["documents"]:
        parent_extracts = extract_by_parent.get(doc["document_id"], [])
        if parent_extracts:
            for extract in parent_extracts:
                unit_rows.append({
                    "retrieval_unit_id": extract["extraction_id"],
                    "parent_document_id": doc["document_id"],
                    "unit_type": extract["unit_type"],
                    "title": (
                        f"{doc['title'].removesuffix(' (first status update)')} "
                        f"(status update {extract['extraction_id'][-2:]}/13)"
                        if extract["unit_type"] == "status_update"
                        else doc["title"]
                    ),
                    "source_type": doc["source_type"],
                    "available_at": extract["content_available_at"],
                    "revised_at": extract["content_revised_at"],
                    "canonical_url": doc["canonical_url"],
                    "timestamp_source_url": doc["timestamp_source_url"],
                    "retrieval_text_archive_path": extract["extracted_text_archive_path"],
                    "retrieval_text_sha256": extract["extracted_content_sha256"],
                    "extraction_id": extract["extraction_id"],
                    "historical_snapshot_status": extract["historical_snapshot_status"],
                    "ingest_status": (
                        "blocked_historical_snapshot_required"
                        if extract["historical_snapshot_status"] == "not_verified_in_this_pass"
                        else "active"
                    ),
                    "notes": extract["notes"],
                })
        else:
            unit_rows.append({
                "retrieval_unit_id": doc["document_id"],
                "parent_document_id": doc["document_id"],
                "unit_type": "primary_source_snapshot",
                "title": doc["title"],
                "source_type": doc["source_type"],
                "available_at": doc["available_at"],
                "revised_at": doc["revised_at"],
                "canonical_url": doc["canonical_url"],
                "timestamp_source_url": doc["timestamp_source_url"],
                "retrieval_text_archive_path": doc["archive_path"],
                "retrieval_text_sha256": doc["content_sha256"],
                "extraction_id": None,
                "historical_snapshot_status": "not_applicable_primary_source_snapshot",
                "ingest_status": "active",
                "notes": "Use the primary source snapshot recorded by the candidate manifest.",
            })
    with RETRIEVAL_UNITS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=unit_fields)
        writer.writeheader()
        writer.writerows(unit_rows)
    manifest["retrieval_units_manifest"] = "数据线/natural_001_retrieval_units_v1.csv"
    manifest["retrieval_unit_count"] = len(unit_rows)
    manifest["follow_up_register"] = "数据线/natural_001_follow_up_register_v1.csv"
    manifest["handoff_record"] = "数据线/natural_001_handoff_v1.md"
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
