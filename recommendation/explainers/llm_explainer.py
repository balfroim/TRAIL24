from typing import List, Optional
from dotenv import load_dotenv
from os import getenv
from langchain.chains.llm import LLMChain
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user_registry import UserRegistry
from recommendation.explainers.abstract_explainer import AbstractExplainer
from recommendation.explainers.traces.llm_trace import LLMTrace
from recommendation.explainers.traces.trance_handler import TraceHandler


class LLMExplainer(AbstractExplainer):
    def __init__(
            self,
            product_registry: ProductRegistry,
            user_registry: UserRegistry,
            rating_registry: RatingRegistry,
            llm_chain: LLMChain
    ):
        super().__init__(product_registry, user_registry, rating_registry)
        self.__llm_chain = llm_chain

    def explain(self, path: RecoPath, filter_facts: Optional[List[str]]=None) -> tuple[str, LLMTrace]:
        bk, product, user = self._prepare_input(path, filter_facts)
        trace_handler = TraceHandler()
        completion = self.__llm_chain.invoke({
            "background_knowledge": bk,
            "user": str(user),
            "product": str(product)
        }, config={"callbacks": [trace_handler]})
        return completion, trace_handler.get_traces()[0]
