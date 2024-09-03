from typing import List, Optional
from langchain.chains.llm import LLMChain
from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user_registry import UserRegistry
from recommendation.explainers.abstract_explainer import AbstractExplainer
from recommendation.explainers.traces.cot_trace import COTTrace
from recommendation.explainers.traces.trance_handler import TraceHandler



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


    def explain(self, path: RecoPath, filter_facts: Optional[List[str]]=None) -> tuple[str, COTTrace]:
        bk, product, user = self._prepare_input(path, filter_facts)
        trace_handler = TraceHandler()
        reasoning_completion = self.__reasoning_chain.invoke({
            "background_knowledge": bk,
            "user": str(user),
            "product_name": str(product)
        }, config={"callbacks": [trace_handler]})
        answering_completion = self.__answering_chain.invoke({
            "reasoning": reasoning_completion,
            "user": str(user),
            "product_name": str(product)
        }, config={"callbacks": [trace_handler]})
        return answering_completion, COTTrace(
            reasoning_trace=trace_handler.get_traces()[0],
            answering_trace=trace_handler.get_traces()[1]
        )

    
