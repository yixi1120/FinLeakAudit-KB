"""Run an embedding-similarity baseline for semantic attribution."""

from __future__ import annotations

import argparse
import csv
import json
import math
import urllib.error
import urllib.request
from pathlib import Path

from config import MODELS


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "experiments" / "analysis"
DEFAULT_INPUT = ANALYSIS_DIR / "semantic_annotation_batch_v1.csv"
DEFAULT_OUTPUT = ANALYSIS_DIR / "semantic_embedding_zhipu_v1.csv"
DEFAULT_METADATA = ANALYSIS_DIR / "semantic_embedding_zhipu_v1.json"
DEFAULT_MODEL = "embedding-3"
DEFAULT_DIMENSIONS = 512


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def parse_pre_cutoff(value: str) -> list[str]:
    try:
        parsed = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []
    if not isinstance(parsed, list):
        return []
    return [
        str(item.get("text", ""))
        for item in parsed
        if isinstance(item, dict) and str(item.get("text", "")).strip()
    ]


def collect_unique_texts(rows: list[dict]) -> list[str]:
    seen = set()
    ordered = []
    for row in rows:
        texts = [
            str(row.get("claim_text", "")),
            str(row.get("post_cutoff_evidence_text", "")),
            *parse_pre_cutoff(row.get("pre_cutoff_evidence", "")),
        ]
        for text in texts:
            if text and text not in seen:
                seen.add(text)
                ordered.append(text)
    return ordered


def cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Embedding dimensions do not match")
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def embed_batch(
    texts: list[str], model: str, dimensions: int
) -> tuple[list[list[float]], dict]:
    config = MODELS["zhipu"]
    payload = {"model": model, "input": texts, "dimensions": dimensions}
    request = urllib.request.Request(
        f"{config.base_url}/embeddings",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(
            request, timeout=config.timeout_seconds
        ) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Embedding call failed: {exc}") from exc
    data = sorted(body["data"], key=lambda item: item["index"])
    if len(data) != len(texts):
        raise ValueError("Embedding API returned an unexpected row count")
    return [item["embedding"] for item in data], body.get("usage", {})


def score_rows(
    rows: list[dict],
    vectors: dict[str, list[float]],
    threshold: float,
    margin_threshold: float,
) -> list[dict]:
    scored = []
    for row in rows:
        claim = str(row.get("claim_text", ""))
        future = str(row.get("post_cutoff_evidence_text", ""))
        future_score = cosine(vectors[claim], vectors[future])
        pre_scores = [
            cosine(vectors[claim], vectors[text])
            for text in parse_pre_cutoff(row.get("pre_cutoff_evidence", ""))
        ]
        max_pre_score = max(pre_scores, default=0.0)
        margin = future_score - max_pre_score
        scored.append(
            {
                "sample_id": row["sample_id"],
                "embedding_prediction": (
                    future_score >= threshold and margin >= margin_threshold
                ),
                "future_embedding_score": round(future_score, 6),
                "max_pre_cutoff_embedding_score": round(max_pre_score, 6),
                "future_minus_pre_embedding_margin": round(margin, 6),
                "threshold": threshold,
                "margin_threshold": margin_threshold,
            }
        )
    return scored


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--dimensions", type=int, default=DEFAULT_DIMENSIONS)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--threshold", type=float, default=0.65)
    parser.add_argument("--margin-threshold", type=float, default=0.03)
    args = parser.parse_args()

    if MODELS["zhipu"].api_key.startswith("missing-"):
        raise RuntimeError("ZHIPU_API_KEY is not configured")
    rows = read_csv(args.input)
    texts = collect_unique_texts(rows)
    vectors = {}
    total_tokens = 0
    for start in range(0, len(texts), args.batch_size):
        batch = texts[start : start + args.batch_size]
        print(
            f"embedding texts {start + 1}-{start + len(batch)} "
            f"of {len(texts)}"
        )
        batch_vectors, usage = embed_batch(batch, args.model, args.dimensions)
        vectors.update(zip(batch, batch_vectors))
        total_tokens += int(usage.get("total_tokens", 0))

    scored = score_rows(
        rows, vectors, args.threshold, args.margin_threshold
    )
    write_csv(args.output, scored)
    metadata = {
        "schema_version": "finleakaudit_semantic_embedding_v1",
        "provider": "zhipu",
        "model": args.model,
        "dimensions": args.dimensions,
        "unique_text_count": len(texts),
        "sample_count": len(rows),
        "total_tokens": total_tokens,
        "threshold": args.threshold,
        "margin_threshold": args.margin_threshold,
        "selection": "pre-specified defaults; not tuned on gold labels",
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output} ({len(scored)} rows)")
    print(f"wrote {args.metadata} ({total_tokens} tokens)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
