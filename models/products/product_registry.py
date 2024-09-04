from typing import List
from models.products.product import Product
from models.products.product_factory import ProductFactory
from models.products.product_row import ProductRow
from models.products.product_mapping_row import ProductMappingRow

  
class ProductRegistry:
    def __init__(self, product_rows: List[ProductRow], product_mapping_rows: List[ProductMappingRow]):
        self.products: List[Product] = ProductFactory().create_products(product_rows, product_mapping_rows)

    def find_by_name(self, name: str) -> Product:
        return next(product for product in self.products if product.name == name)
    
    def find_by_pid(self, pid: int) -> Product:
        return next(product for product in self.products if product.pid == pid)
    
    def find_by_eid(self, entity_id: int) -> Product:
        return next(product for product in self.products if product.eid == entity_id)
    
    