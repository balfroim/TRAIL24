import random
from typing import List

from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_node import RecoNode
from models.reco.reco_path import RecoPath
from models.reco.reco_rel import RecoRel
from models.users.user import User
from models.users.user_registry import UserRegistry
from recommendation.recommenders.abstract_recommender import AbstractRecommender


class RandomRecommender(AbstractRecommender):
    """
    Generates random recommendations for a target user.
    """

    def __init__(self, product_registry: ProductRegistry, user_registry: UserRegistry, rating_registry: RatingRegistry, seed=42):
        super().__init__(product_registry, user_registry, rating_registry)
        random.seed(seed)

    def recommend(self, target_user: User) -> List[RecoPath]:
        #1: gather target_user's ratings
        user_product_pid_set = {
            rating.product.pid
            for rating in self.rating_registry.find_user_ratings(target_user.uid)
        }

        #2: gather other users' ratings of products rated by target_user
        partial_rating_paths = []
        for pid in user_product_pid_set:
            related_user_uids = {
                rating.user.uid
                for rating in self.rating_registry.find_product_ratings(pid)
            }
            for uid in related_user_uids:
                partial_rating_paths.append([target_user.uid, pid, uid])

        #3: gather product ratings by other related users
        complete_rating_paths = []
        for partial_rating_path in partial_rating_paths:
            related_user_uid = partial_rating_path[-1]
            related_product_pids = {
                rating.product.pid
                for rating in self.rating_registry.find_user_ratings(related_user_uid)
            }
            for pid in related_product_pids:
                complete_rating_paths.append([*partial_rating_path, pid])

        #4: filter on unknown products for target user
        filtered_complete_rating_paths = [
            path for path in complete_rating_paths
            if path[-1] not in user_product_pid_set
        ]

        #5: select one at random
        recommended_rating_path = random.choice(filtered_complete_rating_paths)

        #6: build reco path and return
        return [self.__build_reco_path(recommended_rating_path)]

    def __build_reco_path(self, node_list: List[int]) -> RecoPath:
        reco_path = RecoPath([], [])

        for i, node_id in enumerate(node_list):
            if i % 2 == 0:
                reco_node = RecoNode("user", self.user_registry.find_by_uid(node_id).eid)
            else:
                reco_node = RecoNode("product", self.product_registry.find_by_pid(node_id).eid)
                reco_rel = RecoRel(reco_path.nodes[-1], "watched", reco_node)
                reco_path.rels.append(reco_rel)
            reco_path.nodes.append(reco_node)
        return reco_path