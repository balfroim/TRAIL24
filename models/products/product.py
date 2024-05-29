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
    # def __init__(self, product_row: ProductRow, product_mapping_row: ProductMappingRow):
    #     assert product_row.pid == product_mapping_row.rating_id
    #     self.pid = product_row.pid
    #     self.name = product_row.name
    #     self.genre = product_row.genre
    #     super().__init__(product_mapping_row.new_id)