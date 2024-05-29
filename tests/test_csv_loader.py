import pytest
from models.csv_row import csv_row
from models.csv_loader import CSVLoader
# import patch
from unittest.mock import patch
import pandas as pd




class TestCSVLoader:
    def test_read(self):
        @csv_row()
        class MockRow:
            col1: str
            col2: int
        loader = CSVLoader(MockRow, file_path="_")
        with patch("models.csv_loader.pd.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = [pd.DataFrame({"col1": ["value1", "value2"], "col2": [1, 2]})]
            result = loader.read()
            assert result[0].col1 == "value1"
            assert result[0].col2 == 1
            assert result[1].col1 == "value2"
            assert result[1].col2 == 2

    def test_file_path_from_decorator(self):
        @csv_row(file_path="file_path")
        class MockRow:
            col1: str
            col2: int

        loader = CSVLoader(MockRow)
        assert loader.file_path == "file_path"

    def test_no_file_path(self):
        @csv_row()
        class MockRow:
            col1: str
            col2: int

        with pytest.raises(ValueError):
            CSVLoader(MockRow)

    def test_upper_case_cols(self):
        # col in the csv file is in upper case
        # but not in the class
        @csv_row()
        class MockRow:
            col1: str
            col2: int

        loader = CSVLoader(MockRow, file_path="_")
        with patch("models.csv_loader.pd.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = [pd.DataFrame({"COL1": ["value1", "value2"], "COL2": [1, 2]})]
            result = loader.read()
            assert result[0].col1 == "value1"
            assert result[0].col2 == 1
            assert result[1].col1 == "value2"
            assert result[1].col2 == 2

    def test_space_cols(self):
        # col in the csv file has spaces
        # but not in the class it use snake case
        @csv_row()
        class MockRow:
            col_1: str
            col_2: int

        loader = CSVLoader(MockRow, file_path="_")
        with patch("models.csv_loader.pd.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = [pd.DataFrame({"col 1": ["value1", "value2"], "col 2": [1, 2]})]
            result = loader.read()
            assert result[0].col_1 == "value1"
            assert result[0].col_2 == 1
            assert result[1].col_1 == "value2"
            assert result[1].col_2 == 2

    def test_hyphen_cols(self):
        # col in the csv file has hyphens
        # but not in the class it use snake case
        @csv_row()
        class MockRow:
            col_1: str
            col_2: int

        loader = CSVLoader(MockRow, file_path="_")
        with patch("models.csv_loader.pd.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = [pd.DataFrame({"col-1": ["value1", "value2"], "col-2": [1, 2]})]
            result = loader.read()
            assert result[0].col_1 == "value1"
            assert result[0].col_2 == 1
            assert result[1].col_1 == "value2"
            assert result[1].col_2 == 2