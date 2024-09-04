from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class Node:
    eid: int

    @abstractmethod
    def from_rows(self, row, mapping_row):
        raise NotImplementedError
    
    @abstractmethod
    def facts(self):
        raise NotImplementedError