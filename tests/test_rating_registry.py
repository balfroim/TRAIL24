from math import prod

from models.products.product import Product
from models.products.product_mapping_row import ProductMappingRow
from models.products.product_registry import ProductRegistry
from models.products.product_row import ProductRow
from models.ratings.rating_registry import RatingRegistry
from models.ratings.rating_row import RatingRow
from models.users.user import User
from models.users.user_mapping_row import UserMappingRow
from models.users.user_registry import UserRegistry
from models.users.user_row import UserRow


class TestRatingRegistry:
    def test_ratings_from_user(self):
        rating_rows = [RatingRow({'uid': 1, 'pid': 1, 'rating': 5})]
        product_rows = [ProductRow({'pid': 1, 'name': 'test_product'})]
        product_mapping_rows = [ProductMappingRow({'rating_id': 1, 'new_id': 1})]
        product_registry = ProductRegistry(product_rows, product_mapping_rows)
        users = [UserRow({'uid': 1, "genre": "F", 'age': "20"})]
        user_mapping_rows = [UserMappingRow({'rating_id': 1, 'new_id': 1})]
        user_registry = UserRegistry(users, user_mapping_rows)
        rating_registry = RatingRegistry(rating_rows, user_registry, product_registry)
        ratings = rating_registry.find_user_ratings(1)
        assert len(ratings) == 1
        assert ratings[0].rating == 5
        assert ratings[0].user.uid == 1
        assert ratings[0].product.pid == 1

    def test_ratings_from_product(self):
        rating_rows = [RatingRow({'uid': 1, 'pid': 1, 'rating': 5})]
        product_rows = [ProductRow({'pid': 1, 'name': 'test_product'})]
        product_mapping_rows = [ProductMappingRow({'rating_id': 1, 'new_id': 1})]
        product_registry = ProductRegistry(product_rows, product_mapping_rows)
        users = [UserRow({'uid': 1, "genre": "F", 'age': "20"})]
        user_mapping_rows = [UserMappingRow({'rating_id': 1, 'new_id': 1})]
        user_registry = UserRegistry(users, user_mapping_rows)
        rating_registry = RatingRegistry(rating_rows, user_registry, product_registry)
        ratings = rating_registry.find_product_ratings(1)
        assert len(ratings) == 1
        assert ratings[0].rating == 5
        assert ratings[0].user.uid == 1
        assert ratings[0].product.pid == 1

    def test_user_product_rating(self):
        rating_rows = [RatingRow({'uid': 1, 'pid': 1, 'rating': 5})]
        product_rows = [ProductRow({'pid': 1, 'name': 'test_product'})]
        product_mapping_rows = [ProductMappingRow({'rating_id': 1, 'new_id': 1})]
        product_registry = ProductRegistry(product_rows, product_mapping_rows)
        users = [UserRow({'uid': 1, "genre": "F", 'age': "20"})]
        user_mapping_rows = [UserMappingRow({'rating_id': 1, 'new_id': 1})]
        user_registry = UserRegistry(users, user_mapping_rows)
        rating_registry = RatingRegistry(rating_rows, user_registry, product_registry)
        rating = rating_registry.find_user_product_rating(1, 1)
        assert rating.rating == 5
        assert rating.user.uid == 1
        assert rating.product.pid == 1