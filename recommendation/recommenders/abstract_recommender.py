from abc import ABC, abstractmethod
from typing import List

from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user import User
from models.users.user_registry import UserRegistry


class AbstractRecommender(ABC):
    """
    Base class for all recommender methods.
    """

    @abstractmethod
    def __init__(self, product_registry: ProductRegistry, user_registry: UserRegistry, rating_registry: RatingRegistry):
        self.product_registry = product_registry
        self.user_registry = user_registry
        self.rating_registry = rating_registry

    @abstractmethod
    def recommend(self, target_user: User, k: int) -> List[RecoPath]:
        """
        Generate recommendation paths for a target user.

        :param target_user: User target user for recommendation.
        :param k: Number of recommendations.
        :return: List[RecoPath] list of recommendation paths.
        """
        pass
