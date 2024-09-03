from abc import ABC, abstractmethod

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
    def explain(self, path: RecoPath) -> str:
        """
        Generate explanation for o recommendation path.

        :param path: RecoPath.
        :return: str explanation.
        """
        pass

    def generate_facts(self, path: RecoPath) -> str:
        """
        Generate facts for a recommendation path.

        :param path: RecoPath.
        :return: str facts for a recommendation path.
        """
        facts_txt = "% Path: \n"
        for rel in path.rels:
            facts_txt += rel.to_facts() + "\n"
            user = self.user_registry.find_by_eid(rel.in_node.entity_id)
            product = self.product_registry.find_by_eid(rel.out_node.entity_id)
            facts_txt += self.rating_registry.find_user_product_rating(user.uid, product.pid).to_facts() + "\n"
        facts_txt += "% Background Knowledge: \n"
        for node in path.nodes:
            if node.type == "user":
                user = self.user_registry.find_by_eid(node.entity_id)
                facts_txt += user.to_facts() + "\n"
            elif node.type == "product":
                product = self.product_registry.find_by_eid(node.entity_id)
                facts_txt += product.to_facts() + "\n"
        return facts_txt
    
    def _prepare_input(self, path):
        bk = self.generate_facts(path)
        product_eid = path.recommendation[1].entity_id
        product = self.product_registry.find_by_eid(product_eid)
        user_eid = path.recommendation[0].entity_id
        user = self.user_registry.find_by_eid(user_eid)
        return bk,product,user
