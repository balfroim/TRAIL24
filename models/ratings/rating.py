from dataclasses import dataclass

from models.products.product import Product
from models.users.user import User


@dataclass
class Rating:
    user: User
    product: Product
    rating: float