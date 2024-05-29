from typing import List, TypeVar, Generic, Dict, Any

from models.nodes.node import Node

ItemType = TypeVar('ItemType')
MappingRowType = TypeVar('MappingRowType')
RowType = TypeVar('RowType')

class MappingFactory(Generic[ItemType, MappingRowType, RowType]):
    """
    A generic factory class for creating items based on mappings between different rows.

    This class provides a method to create a list of items by mapping rows and mapping rows using specified attributes.
    """

    @staticmethod
    def create_items(rows: List[RowType], mapping_rows: List[MappingRowType], item_cls: Node, id_attr: str, mapping_attr: str) -> List[ItemType]:
        lookup = {getattr(row, id_attr): row for row in rows}
        return [
            item_cls.from_rows(lookup[getattr(mapping_row, mapping_attr)], mapping_row)
            for mapping_row in mapping_rows
        ]