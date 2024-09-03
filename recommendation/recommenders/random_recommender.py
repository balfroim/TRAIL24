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
        # TODO This process need some optimization... ^^
        #1: gather target_user's ratings
        user_ratings = self.rating_registry.find_user_ratings(target_user.uid)
        user_product_pid_set = { rating.product.pid for rating in user_ratings }

        #2: gather other users' ratings of products rated by target_user
        partial_rating_paths = []
        for user_rating in user_ratings:
            product = user_rating.product
            related_ratings = [rating for rating in self.rating_registry.find_product_ratings(product.pid)]
            # remove target_user's ratings
            related_ratings = filter(lambda rating: rating.user.uid != target_user.uid, related_ratings)
            for related_rating in related_ratings:
                partial_rating_paths.append([user_rating, related_rating])

        #3: gather product ratings by other related users
        complete_rating_paths = []
        for partial_rating_path in partial_rating_paths:
            same_product_rating = partial_rating_path[-1]
            related_user_ratings = self.rating_registry.find_user_ratings(same_product_rating.user.uid)
            # remove ratings of products already rated by target_user
            related_user_ratings = filter(lambda rating: rating.product.pid not in user_product_pid_set, related_user_ratings)
            for related_user_rating in related_user_ratings:
                complete_rating_paths.append([*partial_rating_path, related_user_rating])

        #4: select one at random
        recommended_rating_path = random.choice(complete_rating_paths)

        #5: build reco path
        #TODO need to extract this code in another place (SRP)
        reco_path = RecoPath([], [])
        for rating in recommended_rating_path:
            reco_user_node = RecoNode("user", rating.user.eid)
            reco_product_node = RecoNode("product", rating.product.eid)
            reco_path.nodes.append(reco_user_node)
            reco_path.nodes.append(reco_product_node)
            reco_rel = RecoRel(reco_user_node, "watched", reco_product_node)
            reco_path.rels.append(reco_rel)

        #TODO return more than a single recommendation
        return [reco_path]
