from dataclasses import dataclass
from typing import List
from models.products.product_registry import ProductRegistry
from models.ratings.rating import Rating
from models.ratings.rating_factory import RatingFactory
from models.ratings.rating_row import RatingRow
from models.users.user_registry import UserRegistry

class RatingRegistry:
    def __init__(self, ratings: List[RatingRow], user_registry: UserRegistry, product_registry: ProductRegistry):
        self.ratings: List[Rating] = RatingFactory().create_ratings(ratings, user_registry, product_registry)
        self.user_registry = user_registry
        self.product_registry = product_registry

    def find_user_ratings(self, user_id: int) -> List[Rating]:
        return [rating for rating in self.ratings if rating.user.uid == user_id]
    
    def find_product_ratings(self, product_id: int) -> List[Rating]:
        return [rating for rating in self.ratings if rating.product.pid == product_id]
    
    def find_user_product_rating(self, user_id: int, product_id: int) -> Rating:
        return next(rating for rating in self.ratings if rating.user.uid == user_id and rating.product.pid == product_id)