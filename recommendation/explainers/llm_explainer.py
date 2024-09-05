import re
from typing import List, Optional
from langchain.chains.llm import LLMChain
from models.nodes.fact import Fact
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

    def __clean_product_name(self, text: str, name_facts: List[Fact]) -> str: 
        assert all([fact.predicate == "name" for fact in name_facts])
        print(text)
        for fact in name_facts:
            text = re.sub(fact.values[0], f"\"{fact.values[1]}\"", text)
        return text
    
    def __extract_explanation(text):
        """
        Extracts the content between <explanation> and </explanation> tags using regular expressions.

        Args:
            text (str): The input text containing <explanation> and </explanation> tags.

        Returns:
            str: The text between <explanation> and </explanation>, or the input text if the tags are not found.
        """
        pattern = r"(?<=<explanation>)(.|\n)*(?=<\/explanation>)"
        match = re.search(pattern, text)

        if match:
            return match.group(0).strip()
        
        return text

    
    def explain(self, path: RecoPath, exclude_predicates: Optional[List[str]]=None) -> tuple[str, LLMTrace]:
        if exclude_predicates is None:
            exclude_predicates = []
        # TODO maybe we should refactor the context initialization out of the method
        facts = self.fact_collector.collect_facts_from_path(path)
        included_facts, _ = self.fact_collector.exclude_facts(facts, exclude_predicates)
        context = "\n".join([str(fact) for fact in included_facts])
        product, user = self.registry_handler.get_product_and_user(path)
        trace_handler = TraceHandler()
        completion = self.__llm_chain.invoke({
            "context": context,
            "user": str(user),
            "product": str(product)
        }, config={"callbacks": [trace_handler]})
        name_facts = [fact for fact in facts if fact.predicate == "name"]
        completion = self.__clean_product_name(completion, name_facts)
        completion = self.__extract_explanation(completion)
        return completion, trace_handler.get_traces()[0]
