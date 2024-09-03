from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMTrace:
    prompt: str
    completion: Optional[str] = None

    def __str__(self) -> str:
        return f"Prompt: {self.prompt}\nCompletion: {self.completion}"