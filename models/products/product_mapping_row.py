from models.csv_row import csv_row
from paths import PATHS

@csv_row(file_path=PATHS["product_mapping"])
class ProductMappingRow:
    rating_id: int
    new_id: int
