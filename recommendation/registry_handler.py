from models.products.product import Product
from models.products.product_registry import ProductRegistry
from models.ratings.rating import Rating
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user import User
from models.users.user_registry import UserRegistry


class RegistryHandler:
    """
    Handles operations related to accessing entities from registries
    """
    def __init__(self, product_registry: ProductRegistry, user_registry: UserRegistry, rating_registry: RatingRegistry):
        self.product_registry = product_registry
        self.user_registry = user_registry
        self.rating_registry = rating_registry

    def find_product_by_eid(self, eid: str) -> Product:
        return self.product_registry.find_by_eid(eid)

    def find_user_by_eid(self, eid: str) -> User:
        return self.user_registry.find_by_eid(eid)
    
    def get_product_and_user(self, path: RecoPath):
        product_eid = path.recommendation[1].entity_id
        product = self.product_registry.find_by_eid(product_eid)
        user_eid = path.recommendation[0].entity_id
        user = self.user_registry.find_by_eid(user_eid)
        return product, user

    def find_rating_by_eids(self, user_eid: str, product_eid: str) -> Rating:
        user = self.user_registry.find_by_eid(user_eid)
        product = self.product_registry.find_by_eid(product_eid)
        return self.rating_registry.find_user_product_rating(user.uid, product.pid)
