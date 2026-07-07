"""Runtime configuration for FinLeakAudit pilot experiments."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"


@dataclass(frozen=True)
class ModelConfig:
    name: str
    base_url: str
    api_key: str
    model: str
    temperature: float = 0.0
    max_tokens: int = 700
    timeout_seconds: int = 180


def env_or_placeholder(name: str) -> str:
    """Read an API key from the environment without hard-coding secrets."""
    return os.environ.get(name, f"missing-{name}")


MODELS = {
    "qwen": ModelConfig(
        name="qwen",
        base_url="http://127.0.0.1:8080/v1",
        api_key="not-needed",
        model="qwen2.5-14b-instruct-q4_k_m",
    ),
    "deepseek": ModelConfig(
        name="deepseek",
        base_url="https://api.deepseek.com/v1",
        api_key=env_or_placeholder("DEEPSEEK_API_KEY"),
        model="deepseek-chat",
    ),
    "zhipu": ModelConfig(
        name="zhipu",
        base_url="https://open.bigmodel.cn/api/paas/v4",
        api_key=env_or_placeholder("ZHIPU_API_KEY"),
        model="glm-4-flashx-250414",
    ),
}


DEFAULT_CASES_PATH = DATA_DIR / "cases_pilot.jsonl"
