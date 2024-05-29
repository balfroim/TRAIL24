from models.csv_row import csv_row
from paths import PATHS

@csv_row(file_path=PATHS["products"])
class ProductRow:
    pid: int
    name: int
    genre: str