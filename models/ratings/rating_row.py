from models.csv_row import csv_row
from paths import PATHS

@csv_row(file_path=PATHS["ratings"])
class RatingRow:
    uid: int
    pid: int
    rating: float
    timestamp: int
