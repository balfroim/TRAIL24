from typing import List
import pandas as pd
from functools import lru_cache

class CSVLoader:
    def __init__(self, dataclass, file_path: str=None, sep: str = "\t"):
        """
        Initialize with a dataclass type and a file path.
        :param dataclass: The dataclass type to convert rows into.
        :param file_path: The CSV file to read from.
        """
        self.dataclass = dataclass
        if file_path is not None:
            self.file_path = file_path
        elif dataclass.file_path is not None:
            self.file_path = getattr(dataclass, "file_path")
        else:
            raise ValueError("No file path provided.")
        self.sep = sep

    @lru_cache(maxsize=None)
    def __load_df(self) -> pd.DataFrame:
        """
        Load the CSV file into a DataFrame.
        """
        return pd.read_csv(self.file_path, sep=self.sep, header=0, skip_blank_lines=True)

    def read(self) -> List:
        """
        Read the CSV file and return a list of dataclass instances.
        Each row in the DataFrame is converted into an instance of the specified dataclass.
        """
        df = self.__load_df()
        dict_rows = df.to_dict(orient='records')
        dict_rows = [{k.lower().replace(" ", "_").replace("-", "_"): v for k, v in row.items()} for row in dict_rows]
        return [self.dataclass(row) for row in dict_rows]
    