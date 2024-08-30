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


class PersonalizedPageRankRecommender(AbstractRecommender):
    """
    Generates recommendations for a target user.
    Based on Personalized PageRank
    """

    # TODO to implement
    def __init__(self, product_registry: ProductRegistry, user_registry: UserRegistry, rating_registry: RatingRegistry, seed=42):
        super().__init__(product_registry, user_registry, rating_registry)
        pass

    # TODO to implement
    def recommend(self, target_user: User) -> List[RecoPath]:
        pass
