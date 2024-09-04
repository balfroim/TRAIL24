import trace
from typing import List, Optional
from langchain.chains.llm import LLMChain
from models.reco.reco_path import RecoPath
from recommendation.explainers.abstract_explainer import AbstractExplainer
from recommendation.explainers.traces.llm_trace import LLMTrace
from recommendation.explainers.traces.trance_handler import TraceHandler
from recommendation.registry_handler import RegistryHandler


class LLMExplainer(AbstractExplainer):
    def __init__(
            self,
            registry_handler: RegistryHandler,
            llm_chain: LLMChain
    ):
        super().__init__(registry_handler)
        self.__llm_chain = llm_chain

    def explain(self, path: RecoPath, filter_facts: Optional[List[str]]=None) -> tuple[str, LLMTrace]:
        context, product, user = self._prepare_input(path, filter_facts)
        trace_handler = TraceHandler()
        completion = self.__llm_chain.invoke({
            "context": context,
            "user": user,
            "product": product
        }, config={"callbacks": [trace_handler]})
        return completion, trace_handler.get_traces()[0]

