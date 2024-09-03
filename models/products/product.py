from models.nodes.fact import Fact
from models.nodes.node import Node
from models.products.product_row import ProductRow
from models.products.product_mapping_row import ProductMappingRow
from dataclasses import dataclass


@dataclass(frozen=True)
class Product(Node):
    pid: int
    name: str
    genre: str

    @staticmethod
    def from_rows(product_row: ProductRow, product_mapping_row: ProductMappingRow):
        assert product_row.pid == product_mapping_row.rating_id
        return Product(
            pid=product_row.pid,
            name=product_row.name,
            genre=product_row.genre,
            eid=product_mapping_row.new_id
        )
    
    def __str__(self):
        return f"Product{self.eid}"
    
    def facts(self):
        return [
            Fact("name", (str(self), self.name)),
            Fact("genre", (str(self), self.genre))
        ]
    
