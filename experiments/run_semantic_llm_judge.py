"""Run a blinded LLM judge for semantic claim-evidence attribution."""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

from config import MODELS
from semantic_attribution import (
    call_semantic_judge,
    format_evidence,
    normalize_judgment,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "experiments" / "analysis" / "semantic_annotation_batch_v1.csv"
)
DEFAULT_OUTPUT = (
    ROOT / "experiments" / "analysis" / "semantic_llm_judge_deepseek_v1.jsonl"
)

def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def read_completed(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    completed = {}
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                row = json.loads(line)
                completed[row["sample_id"]] = row
    return completed


def parse_pre_cutoff(value: str) -> list[dict]:
    try:
        evidence = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []
    return evidence if isinstance(evidence, list) else []


def format_pre_cutoff(value: str) -> str:
    return format_evidence(parse_pre_cutoff(value))


def call_judge(model_key: str, row: dict) -> dict:
    config = MODELS[model_key]
    judgment = call_semantic_judge(
        config,
        claim=row.get("claim_text", ""),
        pre_cutoff_evidence=parse_pre_cutoff(
            row.get("pre_cutoff_evidence", "")
        ),
        post_cutoff_evidence={
            "text": row.get("post_cutoff_evidence_text", "")
        },
    )
    return {
        "sample_id": row["sample_id"],
        **judgment,
    }


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", choices=["deepseek", "zhipu"], default="deepseek")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    args = parser.parse_args()

    config = MODELS[args.model]
    if config.api_key.startswith("missing-"):
        raise RuntimeError(f"API key for {args.model} is not configured")
    if args.overwrite and args.output.exists():
        args.output.unlink()
    completed = read_completed(args.output)
    rows = read_csv(args.input)
    if args.limit is not None:
        rows = rows[: args.limit]

    pending = [row for row in rows if row["sample_id"] not in completed]
    for index, row in enumerate(pending, start=1):
        print(f"[{index}/{len(pending)}] judging {row['sample_id']} with {args.model}")
        append_jsonl(args.output, call_judge(args.model, row))
        if args.sleep_seconds and index < len(pending):
            time.sleep(args.sleep_seconds)
    total = len(read_completed(args.output))
    print(f"wrote {args.output} ({total} completed rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
