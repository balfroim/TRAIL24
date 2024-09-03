from dataclasses import dataclass
from recommendation.explainers.traces.llm_trace import LLMTrace


@dataclass(frozen=True)
class COTTrace:
    reasoning_trace: LLMTrace
    answering_trace: LLMTrace