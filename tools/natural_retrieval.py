#!/usr/bin/env python3
"""Deterministic text extraction and lexical retrieval for natural events."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "数据线"
BLOCK_TAGS = {
    "article",
    "br",
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "p",
    "section",
    "table",
    "td",
    "th",
    "tr",
}
SKIP_TAGS = {"script", "style", "noscript", "ix:header"}
TOKEN_PATTERN = re.compile(r"[a-z0-9]+", re.IGNORECASE)


class BodyTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        elif not self.skip_depth and tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        elif not self.skip_depth and tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)


def normalize_text(value: str) -> str:
    lines = []
    for line in value.replace("\r", "\n").split("\n"):
        collapsed = " ".join(line.split())
        if collapsed:
            lines.append(collapsed)
    return "\n".join(lines)


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".htm", ".html", ".xml", ".xhtml"}:
        parser = BodyTextParser()
        parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
        text = normalize_text("".join(parser.parts))
    elif suffix in {".txt", ".md", ".csv", ".json"}:
        text = normalize_text(path.read_text(encoding="utf-8", errors="ignore"))
    elif suffix == ".pdf":
        try:
            import fitz
        except ImportError as exc:  # pragma: no cover - environment-dependent
            raise RuntimeError("PDF extraction requires PyMuPDF") from exc
        with fitz.open(path) as document:
            text = normalize_text("\n".join(page.get_text() for page in document))
    else:
        raise ValueError(f"Unsupported retrieval source type: {path}")
    if not text:
        raise ValueError(f"No retrieval text extracted from {path}")
    return text


def chunk_text(text: str, chunk_chars: int = 4000, overlap_chars: int = 300) -> list[str]:
    if chunk_chars <= 0 or not 0 <= overlap_chars < chunk_chars:
        raise ValueError("chunk_chars must be positive and overlap smaller than chunk")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_chars, len(text))
        if end < len(text):
            boundary = text.rfind("\n", start + chunk_chars // 2, end)
            if boundary == -1:
                boundary = text.rfind(" ", start + chunk_chars // 2, end)
            if boundary > start:
                end = boundary
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(start + 1, end - overlap_chars)
    return chunks


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_active_units(event_id: str, as_of: str | None = None) -> list[dict[str, str]]:
    path = DATA / f"{event_id}_retrieval_units_v1.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    cutoff = datetime.fromisoformat(as_of) if as_of else None
    active = []
    for row in rows:
        if row["ingest_status"] != "active":
            continue
        available = datetime.fromisoformat(row["available_at"])
        if cutoff and available > cutoff:
            continue
        source_path = ROOT / row["retrieval_text_archive_path"]
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        if digest(source_path) != row["retrieval_text_sha256"]:
            raise ValueError(f"{row['retrieval_unit_id']}: retrieval source hash mismatch")
        active.append(row)
    return active


def cap_parent_versions(
    rows: list[dict[str, str]], max_units_per_parent: int = 3
) -> list[dict[str, str]]:
    if max_units_per_parent <= 0:
        raise ValueError("max_units_per_parent must be positive")
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["parent_document_id"]].append(row)
    selected = []
    for parent_id in sorted(grouped):
        ordered = sorted(
            grouped[parent_id],
            key=lambda row: (datetime.fromisoformat(row["available_at"]), row["retrieval_unit_id"]),
        )
        selected.extend(ordered[-max_units_per_parent:])
    return selected


def load_candidate_chunks(
    event_id: str,
    as_of: str | None = None,
    max_units_per_parent: int = 3,
    max_chunks_per_unit: int | None = None,
    chunk_chars: int = 4000,
) -> list[dict[str, object]]:
    rows = cap_parent_versions(read_active_units(event_id, as_of), max_units_per_parent)
    output = []
    for row in rows:
        source_path = ROOT / row["retrieval_text_archive_path"]
        chunks = chunk_text(extract_text(source_path), chunk_chars=chunk_chars)
        selected_chunks = chunks if max_chunks_per_unit is None else chunks[:max_chunks_per_unit]
        for index, text in enumerate(selected_chunks, start=1):
            output.append(
                {
                    "chunk_id": f"{row['retrieval_unit_id']}::chunk_{index:03d}",
                    "retrieval_unit_id": row["retrieval_unit_id"],
                    "parent_document_id": row["parent_document_id"],
                    "title": row["title"],
                    "source_type": row["source_type"],
                    "canonical_url": row["canonical_url"],
                    "available_at": row["available_at"],
                    "text": text,
                }
            )
    return output


def tokens(value: str) -> list[str]:
    return TOKEN_PATTERN.findall(value.lower())


def rank_lexical(
    query: str,
    chunks: list[dict[str, object]],
    top_k: int = 8,
    max_chunks_per_parent: int = 2,
) -> list[dict[str, object]]:
    if top_k <= 0 or max_chunks_per_parent <= 0:
        raise ValueError("top_k and max_chunks_per_parent must be positive")
    query_terms = set(tokens(query))
    documents = [tokens(str(chunk["title"]) + " " + str(chunk["text"])) for chunk in chunks]
    document_frequency = Counter(
        term for document in documents for term in set(document) if term in query_terms
    )
    scores = []
    for chunk, document in zip(chunks, documents):
        counts = Counter(document)
        score = 0.0
        for term in query_terms:
            if not counts[term]:
                continue
            inverse_document_frequency = math.log(
                (len(documents) + 1) / (document_frequency[term] + 1)
            ) + 1.0
            score += (1.0 + math.log(counts[term])) * inverse_document_frequency
        scores.append((score, str(chunk["chunk_id"]), chunk))
    scores.sort(key=lambda item: (-item[0], item[1]))

    selected = []
    parent_counts: Counter[str] = Counter()
    for score, _, chunk in scores:
        parent = str(chunk["parent_document_id"])
        if parent_counts[parent] >= max_chunks_per_parent:
            continue
        selected.append({**chunk, "retrieval_score": score})
        parent_counts[parent] += 1
        if len(selected) == top_k:
            break
    return selected


def predictor_view(chunks: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "evidence_id": chunk["chunk_id"],
            "title": chunk["title"],
            "source_type": chunk["source_type"],
            "text": chunk["text"],
        }
        for chunk in chunks
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    parser.add_argument("--as-of")
    parser.add_argument("--top-k", type=int, default=8)
    args = parser.parse_args()

    manifest = json.loads((DATA / f"{args.event}.json").read_text(encoding="utf-8"))
    chunks = load_candidate_chunks(args.event, as_of=args.as_of)
    ranked = rank_lexical(manifest["retrieval_query"], chunks, top_k=args.top_k)
    print(json.dumps(predictor_view(ranked), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
