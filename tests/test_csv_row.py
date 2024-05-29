import pytest
from models.csv_row import csv_row, is_csv_row

@csv_row()
class MockRow:
    col1: str
    col2: int

class TestCSVRow:
    def test_csv_row_initialization(self):
        row_data = {"col1": "Value 1", "col2": 42}
        mock_row = MockRow(row_data)
        assert mock_row.col1 == "Value 1"
        assert mock_row.col2 == 42

    def test_csv_row_conversion(self):
        mock_row = MockRow({"col1": "Value 1", "col2": 42})
        data_dict = mock_row.to_dict()
        assert data_dict == {"col1": "Value 1", "col2": 42}

    def test_is_csv_row(self):
        mock_row = MockRow({"col1": "Value 1", "col2": 42})
        assert is_csv_row(mock_row)

    def test_is_not_class(self):
        with pytest.raises(TypeError):
            @csv_row()
            def _():
                pass
