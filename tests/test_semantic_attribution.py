import json
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from config import ModelConfig  # noqa: E402
from semantic_attribution import call_semantic_judge  # noqa: E402


class SemanticAttributionCallTests(unittest.TestCase):
    def test_transient_network_failure_retries_only_judge_call(self):
        config = ModelConfig(
            name="judge",
            base_url="https://example.invalid/v1",
            api_key="test-key",
            model="judge-v1",
        )
        response_body = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "semantic_dependency": "yes",
                                "relation": "support",
                                "confidence": 0.9,
                                "reason": "Candidate supplies the result.",
                            }
                        )
                    }
                }
            ],
            "usage": {"total_tokens": 10},
        }
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            response_body
        ).encode("utf-8")

        with patch(
            "semantic_attribution.urllib.request.urlopen",
            side_effect=[urllib.error.URLError("reset"), response],
        ) as urlopen:
            judgment = call_semantic_judge(
                config,
                "Current results improved.",
                [{"text": "Historical context."}],
                {"text": "The company reported improved results."},
                max_attempts=2,
                retry_delay=0,
            )

        self.assertEqual(urlopen.call_count, 2)
        self.assertEqual(judgment["semantic_dependency"], "yes")
        self.assertEqual(judgment["usage"]["total_tokens"], 10)


if __name__ == "__main__":
    unittest.main()
