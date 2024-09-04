from langchain_core.callbacks import BaseCallbackHandler
from typing import List
from itertools import chain
from recommendation.explainers.traces.llm_trace import LLMTrace

class TraceHandler(BaseCallbackHandler):
    def __init__(self):
        self.__traces = {}

    def on_llm_start(self, _, prompts: List[str], **kwargs):
        run_id = kwargs["run_id"]
        formatted_prompts = "\n".join(prompts)
        self.__traces[run_id] = LLMTrace(prompt=formatted_prompts)

    def on_llm_end(self, response, **kwargs):
        run_id = kwargs["run_id"]
        completions = chain.from_iterable(response.generations)
        completions_text = "\n".join(completion.text for completion in completions)
        self.__traces[run_id].completion = completions_text
    
    def get_traces(self) -> List[LLMTrace]:
        return list(self.__traces.values())