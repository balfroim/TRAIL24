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

        # inner data structures to optimize find methods
        self.__user_rating_dict = {rating.user.uid:[] for rating in self.ratings}
        self.__product_rating_dict = {rating.product.pid:[] for rating in self.ratings}
        for rating in self.ratings:
            self.__user_rating_dict[rating.user.uid].append(rating)
            self.__product_rating_dict[rating.product.pid].append(rating)

    def find_user_ratings(self, user_id: int) -> List[Rating]:
        return self.__user_rating_dict[user_id]
    
    def find_product_ratings(self, product_id: int) -> List[Rating]:
        return self.__product_rating_dict[product_id]
    
    def find_user_product_rating(self, user_id: int, product_id: int) -> Rating:
        return next(rating for rating in self.__product_rating_dict[product_id] if rating.user.uid == user_id)

    def add_rating(self, rating_data: Rating) -> Rating:
        assert self.user_registry.find_by_uid(rating_data.user.uid) is not None
        new_rating = Rating(
            user=rating_data.user,
            product=rating_data.product,
            rating=rating_data.rating,
            timestamp=rating_data.timestamp,
        )
        self.ratings.append(new_rating)

        # update inner data structures
        if new_rating.user.uid in self.__user_rating_dict:
            self.__user_rating_dict[rating_data.user.uid].append(new_rating)
        else:
            self.__user_rating_dict[rating_data.user.uid] = [new_rating]
        self.__product_rating_dict[rating_data.product.pid].append(new_rating)

        return new_rating

    def delete_rating(self, user_id: int, product_id: int) -> None:
        rating_to_delete = self.find_user_product_rating(user_id, product_id)
        self.ratings.remove(rating_to_delete)
        self.__user_rating_dict[user_id].remove(rating_to_delete)
        self.__product_rating_dict[product_id].remove(rating_to_delete)

        return None
