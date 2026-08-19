"""Prompt templates for the FinLeakAudit pilot."""

from __future__ import annotations


SYSTEM_PROMPT = """You are a financial forecasting analyst. Your task is to predict stock movement based on provided evidence only.

Rules:
1. Use ONLY the evidence provided. Do NOT use outside knowledge.
2. For every claim in your rationale, cite the evidence ID(s) that support it.
3. Choose exactly one prediction: UP, DOWN, or NEUTRAL.
4. Confidence means confidence in your chosen prediction, not probability of UP.
5. If prediction is NEUTRAL, confidence means confidence that the evidence is inconclusive.
6. Do NOT use confidence 0.0 unless you cannot produce a valid assessment.
7. Return valid JSON only. Do not wrap it in Markdown."""


PREDICTION_PROMPT = """Prediction date: {prediction_date}

Available evidence:
{evidence_text}

Task: Predict the stock movement after {prediction_date}.
Choose exactly one prediction: UP, DOWN, or NEUTRAL.

Return this JSON shape:
{{
  "prediction": "UP",
  "confidence": 0.65,
  "rationale": [
    {{
      "claim": "short reasoning statement",
      "evidence_ids": ["e1"],
      "direction": "supports UP"
    }}
  ]
}}

Confidence calibration:
- 0.50: evidence is weak, mixed, or barely sufficient
- 0.60-0.75: evidence moderately supports the chosen prediction
- 0.80-0.95: evidence strongly supports the chosen prediction
- For NEUTRAL, use confidence to express confidence that evidence is inconclusive
- Do not output 0.0 unless no valid assessment is possible."""


NATURAL_PREDICTION_PROMPT = """Company: {company} ({ticker})
Information cutoff: {prediction_cutoff}
Forecast target: stock-price direction from the cutoff close to the {forecast_horizon}.

Available evidence:
{evidence_text}

Task: Predict the target-period stock movement using only the evidence above.
Choose exactly one prediction: UP, DOWN, or NEUTRAL.

Return this JSON shape:
{{
  "prediction": "UP",
  "confidence": 0.65,
  "rationale": [
    {{
      "claim": "short reasoning statement",
      "evidence_ids": ["evidence_id"],
      "direction": "supports UP"
    }}
  ]
}}

Confidence calibration:
- 0.50: evidence is weak, mixed, or barely sufficient
- 0.60-0.75: evidence moderately supports the chosen prediction
- 0.80-0.95: evidence strongly supports the chosen prediction
- For NEUTRAL, use confidence to express confidence that evidence is inconclusive
- Do not output 0.0 unless no valid assessment is possible."""


def format_evidence(evidence: list[dict]) -> str:
    return "\n".join(f'- {ev["id"]} | {ev["text"]}' for ev in evidence)


def build_prediction_prompt(case: dict, evidence: list[dict]) -> str:
    return PREDICTION_PROMPT.format(
        prediction_date=case["prediction_date"],
        evidence_text=format_evidence(evidence),
    )


def build_natural_prediction_prompt(case: dict, evidence: list[dict]) -> str:
    return NATURAL_PREDICTION_PROMPT.format(
        company=case["company"],
        ticker=case["ticker"],
        prediction_cutoff=case["prediction_cutoff"],
        forecast_horizon=case["forecast_horizon"],
        evidence_text=format_evidence(evidence),
    )
