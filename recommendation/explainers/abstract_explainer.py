from abc import ABC, abstractmethod
from ast import Not
from typing import List, Optional

from regex import F

from models.nodes.fact import Fact
from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users import user
from models.users.user_registry import UserRegistry
from recommendation.facts.fact_collector import FactCollector
from recommendation.registry_handler import RegistryHandler


class AbstractExplainer(ABC):
    """
    Base class for all explainer methods.
    """

    @abstractmethod
    def __init__(self, registry_handler: RegistryHandler):
        self.registry_handler = registry_handler
        self.fact_collector = FactCollector(registry_handler)

    @abstractmethod
    def explain(self, path: RecoPath, filter_facts: Optional[List[str]]=None) -> str:
        """
        Generate explanation for a recommendation path.

        :param path: RecoPath.
        :return: str explanation.
        """
        raise NotImplementedError
    
    def _prepare_input(self, path: RecoPath, filter_facts:Optional[List[str]]=None):
        facts = self.fact_collector.collect_facts_from_path(path)
        filtered_facts = self.fact_collector.filter_facts(facts, filter_facts)
        context = "\n".join([str(f) for f in filtered_facts])
        product, user = self.registry_handler.get_product_and_user(path)
        return context, str(product), str(user)
