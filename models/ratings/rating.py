from dataclasses import dataclass
from models.nodes.fact import Fact
from models.products.product import Product
from models.users.user import User


@dataclass
class Rating:
    user: User
    product: Product
    rating: float
    timestamp: int

    def facts(self):
        return [
            Fact("rated", (str(self.user), str(self.product), str(self.rating)))
        ]