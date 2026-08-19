#!/usr/bin/env python3
"""Run an offline top-k smoke test across all frozen natural events."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from natural_retrieval import load_candidate_chunks, rank_lexical


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "数据线"
OUTPUT = DATA / "natural_retrieval_smoke_v1.csv"


def main() -> int:
    rows = []
    for manifest_path in sorted(DATA.glob("natural_0[0-9][0-9].json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        chunks = load_candidate_chunks(
            manifest["event_id"], as_of=manifest["outcome_time"]
        )
        ranked = rank_lexical(manifest["retrieval_query"], chunks, top_k=8)
        event_chunks = [
            str(row["chunk_id"])
            for row in ranked
            if row["parent_document_id"] == manifest["event_parent_document_id"]
        ]
        rows.append(
            {
                "event_id": manifest["event_id"],
                "retrieval_as_of": manifest["outcome_time"],
                "candidate_chunks_as_of_outcome": len(chunks),
                "top_k": len(ranked),
                "unique_parents": len(
                    {str(row["parent_document_id"]) for row in ranked}
                ),
                "event_source_group_in_top_k": bool(event_chunks),
                "event_source_chunk_ids": "|".join(event_chunks),
                "top_chunk_ids": "|".join(str(row["chunk_id"]) for row in ranked),
            }
        )
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    hits = sum(bool(row["event_source_group_in_top_k"]) for row in rows)
    print(f"wrote {OUTPUT}: event-source group reached top-8 in {hits}/{len(rows)} events")
    return 0 if hits == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
