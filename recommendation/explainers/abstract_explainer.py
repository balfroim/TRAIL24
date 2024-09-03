from abc import ABC, abstractmethod
from ast import Not
from typing import List, Optional

from regex import F

from models.nodes.fact import Fact
from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user_registry import UserRegistry


class AbstractExplainer(ABC):
    """
    Base class for all explainer methods.
    """

    @abstractmethod
    def __init__(self, product_registry: ProductRegistry, user_registry: UserRegistry, rating_registry: RatingRegistry):
        self.product_registry = product_registry
        self.user_registry = user_registry
        self.rating_registry = rating_registry

    @abstractmethod
    def explain(self, path: RecoPath, filter_facts: Optional[List[str]]=None) -> str:
        """
        Generate explanation for o recommendation path.

        :param path: RecoPath.
        :return: str explanation.
        """
        raise NotImplementedError

    def collect_facts(self, path: RecoPath) -> List[Fact]:
        facts = []
        for rel in path.rels:
            facts.extend(rel.facts())
            user = self.user_registry.find_by_eid(rel.in_node.entity_id)
            product = self.product_registry.find_by_eid(rel.out_node.entity_id)
            rating = self.rating_registry.find_user_product_rating(user.uid, product.pid)
            facts.extend(rating.facts())
        for node in path.nodes:
            if node.type == "user":
                user = self.user_registry.find_by_eid(node.entity_id)
                facts.extend(user.facts())
            elif node.type == "product":
                product = self.product_registry.find_by_eid(node.entity_id)
                facts.extend(product.facts())
        return facts
    
    def _prepare_input(self, path, filter_facts:Optional[List[str]]=None):
        facts = self.collect_facts(path)
        if filter_facts:
            facts = [f for f in facts if f.predicate not in filter_facts]
        bk = "\n".join([str(f) for f in facts])
        product_eid = path.recommendation[1].entity_id
        product = self.product_registry.find_by_eid(product_eid)
        user_eid = path.recommendation[0].entity_id
        user = self.user_registry.find_by_eid(user_eid)
        return bk,product,user
