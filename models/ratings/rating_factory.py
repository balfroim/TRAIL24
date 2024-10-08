from typing import List

from models.cache_to_file import cache_to_file
from models.products.product_registry import ProductRegistry
from models.ratings.rating import Rating
from models.ratings.rating_row import RatingRow
from models.users.user_registry import UserRegistry


class RatingFactory:
    @staticmethod
    @cache_to_file("ratings.pkl")
    def create_ratings(rating_rows: List[RatingRow], user_registry: UserRegistry, product_registry: ProductRegistry) -> List[Rating]:
        return [
            Rating(user_registry.find_by_uid(rating_row.uid), product_registry.find_by_pid(rating_row.pid), rating_row.rating, rating_row.timestamp)
            for rating_row in rating_rows
        ]
