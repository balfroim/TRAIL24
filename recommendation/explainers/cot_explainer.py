import itertools
from typing import List, Optional
from attr import dataclass
from langchain.chains.llm import LLMChain
from dataclasses import dataclass
from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user_registry import UserRegistry
from recommendation.explainers.abstract_explainer import AbstractExplainer
from langchain_core.callbacks import BaseCallbackHandler


@dataclass
class LLMTrace:
    prompt: str
    completion: Optional[str] = None

    def __str__(self) -> str:
        return f"Prompt: {self.prompt}\nCompletion: {self.completion}"
    
@dataclass(frozen=True)
class COTTrace:
    reasoning_trace: LLMTrace
    answering_trace: LLMTrace

class TraceHandler(BaseCallbackHandler):
    def __init__(self):
        self.__traces = {}

    def on_llm_start(self, _, prompts: List[str], **kwargs):
        run_id = kwargs["run_id"]
        formatted_prompts = "\n".join(prompts)
        self.__traces[run_id] = LLMTrace(prompt=formatted_prompts)

    def on_llm_end(self, response, **kwargs):
        run_id = kwargs["run_id"]
        completions = itertools.chain.from_iterable(response.generations)
        completions_text = "\n".join(completion.text for completion in completions)
        self.__traces[run_id].completion = completions_text
    
    def get_traces(self) -> List[LLMTrace]:
        return list(self.__traces.values())


class COTExplainer(AbstractExplainer):
    def __init__(
            self,
            product_registry: ProductRegistry,
            user_registry: UserRegistry,
            rating_registry: RatingRegistry,
            reasoning_chain: LLMChain,
            answering_chain: LLMChain
    ):
        super().__init__(product_registry, user_registry, rating_registry)
        self.__reasoning_chain = reasoning_chain
        self.__answering_chain = answering_chain


    def explain(self, path: RecoPath) -> tuple[str, COTTrace]:
        bk, product, user = self._prepare_input(path)
        trace_handler = TraceHandler()
        reasoning_completion = self.__reasoning_chain.invoke({
            "background_knowledge": bk,
            "user": str(user),
            "product_name": product.name
        }, config={"callbacks": [trace_handler]})
        answering_completion = self.__answering_chain.invoke({
            "reasoning": reasoning_completion,
            "user": str(user),
            "product_name": product.name
        }, config={"callbacks": [trace_handler]})
        return answering_completion, COTTrace(
            reasoning_trace=trace_handler.get_traces()[0],
            answering_trace=trace_handler.get_traces()[1]
        )

    
