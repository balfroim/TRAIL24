import random
import networkx as nx
from typing import List

from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_node import RecoNode
from models.reco.reco_path import RecoPath
from models.reco.reco_rel import RecoRel
from models.users.user import User
from models.users.user_registry import UserRegistry
from recommendation.recommenders.abstract_recommender import AbstractRecommender


class PersonalizedPageRankRecommender(AbstractRecommender):
    """
    Generates recommendations for a target user.
    Based on Personalized PageRank
    """

    def __init__(self, product_registry: ProductRegistry, user_registry: UserRegistry, rating_registry: RatingRegistry, seed=42):
        super().__init__(product_registry, user_registry, rating_registry)
        random.seed(seed)

        self.G = nx.Graph()
        user_eids = [user.eid for user in user_registry.users]
        self.G.add_nodes_from(user_eids, type="user")
        product_eids = [product.eid for product in product_registry.products]
        self.G.add_nodes_from(product_eids, type="product")
        rating_edge_tuples = [(rating.user.eid, rating.product.eid) for rating in rating_registry.ratings]
        self.G.add_edges_from(rating_edge_tuples)

    def recommend(self, target_user: User, k=1) -> List[RecoPath]:
        ratings = self.rating_registry.find_user_ratings(target_user.uid)
        # Update graph with user if needed
        if target_user.eid not in self.G:
            self.G.add_node(target_user.eid, type="user")
        rating_edge_tuples = [(rating.user.eid, rating.product.eid) for rating in ratings]
        self.G.add_edges_from(rating_edge_tuples)

        # Prepare computation
        seed_product_eid_set = {rating.product.eid for rating in ratings}
        # seed_items = random.sample(candidate_pref_items_set, 3)
        seed_dict = { eid: 1 / len(seed_product_eid_set) for eid in seed_product_eid_set}

        # Compute Personalized PageRank
        pagerank_results = nx.pagerank(self.G, personalization=seed_dict)
        filtered_pagerank_results = filter(
            lambda i: self.G.nodes[i[0]]["type"] == "product" and i[0] not in seed_product_eid_set,
            pagerank_results.items())
        rec_product_eids = [t[0] for t in sorted(filtered_pagerank_results, key=lambda i: -i[1])[:k]]

        # Paths Computation
        graph_paths = []
        for product_eid in rec_product_eids:
            graph_paths.append(nx.shortest_path(self.G, source=target_user.eid, target=product_eid))

        # Build reco path and return
        return [self.__build_reco_path(path) for path in graph_paths]

    def __build_reco_path(self, node_list: List[int]) -> RecoPath:
        reco_path = RecoPath([], [])

        for i, node_id in enumerate(node_list):
            if i % 2 == 0:
                reco_node = RecoNode("user", self.user_registry.find_by_eid(node_id).eid)
            else:
                reco_node = RecoNode("product", self.product_registry.find_by_eid(node_id).eid)
                reco_rel = RecoRel(reco_path.nodes[-1], "watched", reco_node)
                reco_path.rels.append(reco_rel)
            reco_path.nodes.append(reco_node)
        return reco_path