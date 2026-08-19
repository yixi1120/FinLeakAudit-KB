#!/usr/bin/env python3
"""Create the mandatory independent source-verification batch."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "数据线"
OUTPUT = DATA / "natural_second_verification_batch_v1.csv"


def deterministic_sample(rows: list[dict[str, object]], count: int) -> list[dict[str, object]]:
    return sorted(
        rows,
        key=lambda row: hashlib.sha256(
            f"finleakaudit-second-verifier-v1:{row['event_id']}:{row['document_id']}".encode()
        ).hexdigest(),
    )[:count]


def build_batch(manifests: list[dict[str, object]]) -> list[dict[str, object]]:
    selected = []
    for manifest in manifests:
        cutoff = datetime.fromisoformat(str(manifest["prediction_cutoff"]))
        pre_cutoff = []
        mandatory = []
        for document in manifest["documents"]:
            row = {
                "event_id": manifest["event_id"],
                "document_id": document["document_id"],
                "prediction_cutoff": manifest["prediction_cutoff"],
                "title": document["title"],
                "source_url": document["source_url"],
                "available_at": document["available_at"] or "",
                "timestamp_source_url": document["timestamp_source_url"] or "",
                "archive_path": document["archive_path"],
                "content_sha256": document["content_sha256"],
            }
            if not document["available_at"]:
                row["sampling_reason"] = "mandatory_unresolved_timestamp"
                mandatory.append(row)
            elif datetime.fromisoformat(document["available_at"]) > cutoff:
                row["sampling_reason"] = "mandatory_post_cutoff"
                mandatory.append(row)
            else:
                row["sampling_reason"] = "sampled_pre_cutoff_20_percent"
                pre_cutoff.append(row)
        sample_count = max(1, math.ceil(len(pre_cutoff) * 0.20))
        selected.extend(mandatory)
        selected.extend(deterministic_sample(pre_cutoff, sample_count))

    output = []
    for row in sorted(selected, key=lambda item: (item["event_id"], item["document_id"])):
        output.append(
            {
                **row,
                "second_verifier_id": "",
                "url_content_match": "",
                "timestamp_evidence_match": "",
                "archive_hash_match": "",
                "decision": "",
                "verification_notes": "",
                "verified_at": "",
            }
        )
    return output


def main() -> int:
    manifests = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(DATA.glob("natural_0[0-9][0-9].json"))
    ]
    rows = build_batch(manifests)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUTPUT} ({len(rows)} rows requiring independent review)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
