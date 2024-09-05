from typing import List, Optional
from langchain.chains.llm import LLMChain
from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user_registry import UserRegistry
from recommendation.explainers.abstract_explainer import AbstractExplainer
from recommendation.explainers.traces.cot_trace import COTTrace
from recommendation.explainers.traces.trace_handler import TraceHandler
from recommendation.registry_handler import RegistryHandler


# FIXME: legacy code, should be refactored or removed
class COTExplainer(AbstractExplainer):
    def __init__(
            self,
            registry_handler: RegistryHandler,
            reasoning_chain: LLMChain,
            answering_chain: LLMChain
    ):
        super().__init__(registry_handler)
        self.__reasoning_chain = reasoning_chain
        self.__answering_chain = answering_chain


    def explain(self, path: RecoPath, filter_facts: Optional[List[str]]=None) -> tuple[str, COTTrace]:
        context, product, user = self._prepare_input(path, filter_facts)
        trace_handler = TraceHandler()
        reasoning_completion = self.__reasoning_chain.invoke({
            "context": context,
            "user": user,
            "product": product
        }, config={"callbacks": [trace_handler]})
        answering_completion = self.__answering_chain.invoke({
            "reasoning": reasoning_completion,
            "user": user,
            "product": product
        }, config={"callbacks": [trace_handler]})
        return answering_completion, COTTrace(
            reasoning_trace=trace_handler.get_traces()[0],
            answering_trace=trace_handler.get_traces()[1]
        )

    
