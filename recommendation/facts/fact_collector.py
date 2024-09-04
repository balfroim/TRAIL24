from typing import List, Optional
from models.nodes.fact import Fact
from models.reco.reco_node import RecoNode
from models.reco.reco_path import RecoPath
from models.reco.reco_rel import RecoRel
from recommendation.registry_handler import RegistryHandler


class FactCollector:
    """
    Responsible for collecting facts from paths, users, products, and ratings.
    """
    def __init__(self, registry_handler: RegistryHandler):
        self.registry_handler = registry_handler

    def collect_facts_from_path(self, path: RecoPath) -> List[Fact]:
        facts = []
        for rel in path.rels:
            facts.extend(self._collect_facts_from_relation(rel))
        for node in path.nodes:
            facts.extend(self._collect_facts_from_node(node))
        return facts

    def _collect_facts_from_relation(self, rel: RecoRel) -> List[Fact]:
        facts = []
        facts.extend(rel.facts())
        rating = self.registry_handler.find_rating_by_eids(rel.in_node.entity_id, rel.out_node.entity_id)
        facts.extend(rating.facts())
        return facts

    def _collect_facts_from_node(self, node: RecoNode) -> List[Fact]:
        facts = []
        if node.type == "user":
            user = self.registry_handler.find_user_by_eid(node.entity_id)
            facts.extend(user.facts())
        elif node.type == "product":
            product = self.registry_handler.find_product_by_eid(node.entity_id)
            facts.extend(product.facts())
        return facts

    def filter_facts(self, facts: List[Fact], filter_facts: Optional[List[str]]) -> List[Fact]:
        if filter_facts:
            return [f for f in facts if f.predicate not in filter_facts]
        return facts