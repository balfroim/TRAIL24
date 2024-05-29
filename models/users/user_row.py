from models.csv_row import csv_row
from paths import PATHS

@csv_row(file_path=PATHS["users"])
class UserRow:
    uid: int
    gender: str
    age: str
