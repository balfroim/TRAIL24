from typing import List, Optional
from models.nodes.fact import Fact
from models.reco.reco_node import RecoNode
from models.reco.reco_path import RecoPath
from models.reco.reco_rel import RecoRel
from recommendation.registry_handler import RegistryHandler
from itertools import tee

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

    def exclude_facts(self, facts: List[Fact], exclude_predicates: List[str]) -> tuple[List[Fact], List[Fact]]:
        """
        Splits the facts into two lists based on the predicate.
        
        :param facts: List of Fact objects.
        :param exclude_predicates: List of predicates to exclude.
        :return: Tuple of two lists:
                    - first: List of facts that are not excluded.
                    - second: List of facts that are excluded.
        
        Example:
        --------
        facts = [Fact("name", ("user1", "John")), Fact("age", ("user1", "25"))]
        exclude_predicates = ["name"]
        result = ([Fact("age", ("user1", "25"))], [Fact("name", ("user1", "John"))])
        """
        # Duplicate the facts iterator for two independent iterations
        included_iter, excluded_iter = tee(facts)
        
        def is_excluded(fact: Fact) -> bool:
            """Helper function to check if a fact's predicate should be excluded."""
            return fact.predicate in exclude_predicates
        
        is_included = lambda fact: not is_excluded(fact)
        included_facts = list(filter(is_included, included_iter))
        excluded_facts = list(filter(is_excluded, excluded_iter))
        return included_facts, excluded_facts