from typing import List

from models.products.product_registry import ProductRegistry
from models.ratings.rating import Rating
from models.ratings.rating_row import RatingRow
from models.users.user_registry import UserRegistry


class RatingFactory:
    @staticmethod
    def create_ratings(rating_rows: List[RatingRow], user_registry: UserRegistry, product_registry: ProductRegistry) -> List[Rating]:
        return [
            Rating(user_registry.find_by_uid(rating_row.uid), product_registry.find_by_pid(rating_row.pid), rating_row.rating)
            for rating_row in rating_rows
        ]
