"""Optional local LLM client for Ollama.

The core agent never depends on this file. If Ollama is not running, the
pipeline falls back to the template note.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any

import requests

from sla.utils.errors import LLMError

PROMPT_TEMPLATE = """You explain the results of a reinforcement-learning training run to students.
Write 3 to 5 short sentences in plain English.
Rules:
- Use ONLY numbers that appear in the FACTS below. Do not calculate new numbers.
- Do not invent results, causes or future predictions.
- If the change is positive, say the reward improved; if negative, say it fell.

FACTS (JSON):
{facts}
"""


def build_prompt(facts: dict[str, Any]) -> str:
    return PROMPT_TEMPLATE.format(facts=json.dumps(facts, indent=2))


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None,
                 timeout: float = 60.0, retries: int = 2) -> None:
        self.base_url = (base_url or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.model = model or os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b")
        self.timeout = timeout
        self.retries = retries

    def is_available(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/api/tags", timeout=3).ok
        except requests.RequestException:
            return False

    def generate(self, prompt: str) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False, "options": {"temperature": 0}}
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                resp = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=self.timeout)
                resp.raise_for_status()
                text = resp.json().get("response", "").strip()
                if not text:
                    raise LLMError("Ollama returned an empty response")
                return text
            except (requests.RequestException, ValueError, LLMError) as exc:
                last_error = exc
                time.sleep(min(2 ** attempt, 4))
        raise LLMError(f"Ollama request failed after {self.retries + 1} attempts: {last_error}")
