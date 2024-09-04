from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Fact:
    predicate: str
    values: Tuple[str]

    def __str__(self):
        values = [f'"{value}"' if ' ' in value else value for value in self.values]
        return f"{self.predicate}({', '.join(values)})"