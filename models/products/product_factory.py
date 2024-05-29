from typing import List

from models.mapping_factory import MappingFactory
from models.products.product import Product
from models.products.product_mapping_row import ProductMappingRow
from models.products.product_row import ProductRow


class ProductFactory(MappingFactory['Product', 'ProductMappingRow', 'ProductRow']):
    @staticmethod
    def create_products(product_rows: List['ProductRow'], product_mapping_rows: List['ProductMappingRow']) -> List['Product']:
        return MappingFactory.create_items(product_rows, product_mapping_rows, Product, 'pid', 'rating_id')
