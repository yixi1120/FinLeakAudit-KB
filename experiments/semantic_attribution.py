"""Shared blinded semantic claim-evidence attribution utilities."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from config import ModelConfig


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


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise


def format_evidence(items: list[dict]) -> str:
    """Format evidence text without exposing IDs or timestamp metadata."""
    lines = [
        f"- {item.get('text', '')}"
        for item in items
        if isinstance(item, dict) and str(item.get("text", "")).strip()
    ]
    return "\n".join(lines) if lines else "(none)"


def build_semantic_prompt(
    claim: str,
    pre_cutoff_evidence: list[dict],
    post_cutoff_evidence: dict,
) -> str:
    return USER_PROMPT.format(
        claim=claim,
        pre_cutoff=format_evidence(pre_cutoff_evidence),
        post_cutoff=post_cutoff_evidence.get("text", ""),
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


def call_semantic_judge(
    config: ModelConfig,
    claim: str,
    pre_cutoff_evidence: list[dict],
    post_cutoff_evidence: dict,
    max_attempts: int = 3,
    retry_delay: float = 1.0,
) -> dict:
    prompt = build_semantic_prompt(
        claim,
        pre_cutoff_evidence,
        post_cutoff_evidence,
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
    body = None
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(
                request, timeout=config.timeout_seconds
            ) as response:
                body = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt < max_attempts:
                time.sleep(retry_delay * attempt)
    if body is None:
        raise RuntimeError(
            f"Semantic judge call failed after {max_attempts} attempts: "
            f"{last_error}"
        ) from last_error
    content = body["choices"][0]["message"]["content"]
    return {
        **normalize_judgment(extract_json(content)),
        "judge_model": config.name,
        "judge_model_id": config.model,
        "usage": body.get("usage", {}),
        "raw_content": content,
    }
