from models.products.product_registry import ProductRegistry
from models.products.product_mapping_row import ProductMappingRow
from models.products.product_row import ProductRow


class TestProductRegistry:
    def test_find_by_pid(self):
        products = [ProductRow({'pid': 1, 'name': 'test_product'})]
        product_mapping_rows = [ProductMappingRow({'rating_id': 1, 'new_id': 1})]
        product_registry = ProductRegistry(products, product_mapping_rows)
        product = product_registry.find_by_pid(1)
        assert product.eid == 1
        assert product.pid == 1
        assert product.name == 'test_product'

    def test_find_by_name(self):
        products = [ProductRow({'pid': 1, 'name': 'test_product'})]
        product_mapping_rows = [ProductMappingRow({'rating_id': 1, 'new_id': 1})]
        product_manager = ProductRegistry(products, product_mapping_rows)
        product = product_manager.find_by_name('test_product')
        assert product.eid == 1
        assert product.pid == 1
        assert product.name == 'test_product'