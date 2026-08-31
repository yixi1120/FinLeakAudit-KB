"""Run a blinded LLM judge for semantic claim-evidence attribution."""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from config import MODELS
from run_experiment import extract_json


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "experiments" / "analysis" / "semantic_annotation_batch_v1.csv"
)
DEFAULT_OUTPUT = (
    ROOT / "experiments" / "analysis" / "semantic_llm_judge_deepseek_v1.jsonl"
)

SYSTEM_PROMPT = """You are evaluating claim-evidence attribution, not stock performance.

Decide whether the claim semantically depends on the candidate post-cutoff evidence. A dependency exists when the candidate evidence supplies a core fact, number, event, or conclusion used by the claim that is not already supported by the pre-cutoff evidence. Mere topical similarity is not dependency. If pre-cutoff evidence already supports the same core content, answer no. Use uncertain only when the evidence genuinely does not permit a reliable decision.

Return valid JSON only. Do not use outside knowledge."""

USER_PROMPT = """Forecast rationale claim:
{claim}

Evidence available before the cutoff:
{pre_cutoff}

Candidate evidence published after the cutoff:
{post_cutoff}

Return exactly this JSON shape:
{{
  "semantic_dependency": "yes | no | uncertain",
  "relation": "support | contradict | irrelevant | uncertain",
  "confidence": 0.0,
  "reason": "one short evidence-grounded sentence"
}}"""


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


def format_pre_cutoff(value: str) -> str:
    try:
        evidence = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        evidence = []
    if not evidence:
        return "(none)"
    return "\n".join(
        f"- {item.get('text', '')}" for item in evidence if isinstance(item, dict)
    )


def normalize_judgment(parsed: dict) -> dict:
    dependency = str(parsed.get("semantic_dependency", "uncertain")).lower()
    if dependency not in {"yes", "no", "uncertain"}:
        dependency = "uncertain"
    relation = str(parsed.get("relation", "uncertain")).lower()
    if relation not in {"support", "contradict", "irrelevant", "uncertain"}:
        relation = "uncertain"
    try:
        confidence = float(parsed.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    return {
        "semantic_dependency": dependency,
        "relation": relation,
        "confidence": max(0.0, min(1.0, confidence)),
        "reason": str(parsed.get("reason", "")).strip(),
    }


def call_judge(model_key: str, row: dict) -> dict:
    config = MODELS[model_key]
    prompt = USER_PROMPT.format(
        claim=row.get("claim_text", ""),
        pre_cutoff=format_pre_cutoff(row.get("pre_cutoff_evidence", "")),
        post_cutoff=row.get("post_cutoff_evidence_text", ""),
    )
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
        "max_tokens": 300,
    }
    request = urllib.request.Request(
        f"{config.base_url}/chat/completions",
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
        raise RuntimeError(f"Judge call failed: {exc}") from exc
    content = body["choices"][0]["message"]["content"]
    judgment = normalize_judgment(extract_json(content))
    return {
        "sample_id": row["sample_id"],
        "judge_model": model_key,
        "judge_model_id": config.model,
        **judgment,
        "usage": body.get("usage", {}),
        "raw_content": content,
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
