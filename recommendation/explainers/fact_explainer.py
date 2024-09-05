import re
from typing import List
from models.nodes.fact import Fact
from recommendation.explainers.abstract_explainer import AbstractExplainer
from recommendation.explainers.traces.trace_handler import TraceHandler
from recommendation.facts.fact_collector import FactCollector
from recommendation.registry_handler import RegistryHandler
from langchain.chains.llm import LLMChain

class FactExplainer(AbstractExplainer):
    def __init__(self, registry_handler: RegistryHandler, llm_chain: LLMChain, **kwargs):
        super().__init__(registry_handler, **kwargs)
        self.__llm_chain = llm_chain
        self.__fact_collector = FactCollector(registry_handler)
        self.__trace_handler = TraceHandler()

    def _preprocess(self, **kwargs):
        # if exclude_predicates is None:
        #     exclude_predicates = []
        path = kwargs.get("path")
        if path is None:
            raise ValueError("Path argument is required for preprocessing.")
        exclude_predicates = kwargs.get("exclude_predicates", [])
        facts = self.__fact_collector.collect_facts_from_path(path)
        included_facts, _ = self.__fact_collector.exclude_facts(facts, exclude_predicates)
        context = "\n".join([str(fact) for fact in included_facts])
        product, user = self.registry_handler.get_product_and_user(path)
        return {"context": context, "user": str(user), "product": str(product)}
    
    def _process(self, input, **_):
        return self.__llm_chain.invoke(input, config={"callbacks": [self.__trace_handler]})
    
    def __clean_product_name(self, text: str, name_facts: List[Fact]) -> str: 
        assert all([fact.predicate == "name" for fact in name_facts])
        for fact in name_facts:
            text = re.sub(fact.values[0], f"\"{fact.values[1]}\"", text)
        return text
    
    def __extract_explanation(self, text):
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
    
    def _postprocess(self, completion, **kwargs):
        path = kwargs.get("path")
        if path is None:
            raise ValueError("Path argument is required for postprocessing.")
        facts = self.__fact_collector.collect_facts_from_path(path)
        name_facts = [fact for fact in facts if fact.predicate == "name"]
        completion = self.__clean_product_name(completion, name_facts)
        completion = self.__extract_explanation(completion)
        return completion
    
    # def explain(self, path, exclude_predicates=None, **kwargs):
    #     return super().explain(path=path, exclude_predicates=exclude_predicates, **kwargs)