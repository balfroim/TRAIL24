from dataclasses import dataclass, fields, is_dataclass
from typing import Dict, Any, Type, Callable, Optional


def csv_row(file_path: str = None) -> Type[Any]:
    """
    Decorator to enhance a dataclass with CSV row initialization and conversion capabilities.
    Assumes that the class is a dataclass and that keys in the input dictionary match the dataclass fields.
    """
    def decorator(cls: Type[Any]) -> Type[Any]:
        if not isinstance(cls, type):
            print(cls)
            raise TypeError("Expected a class, got {}".format(type(cls).__name__))
        if not is_dataclass(cls):
            cls = dataclass(cls)
        
        original_init = cls.__init__

        def __init__(self, row: Dict[str, Any]):
            """
            Initialize the dataclass with data from a CSV row.
            """
            for field in fields(cls):
                setattr(self, field.name, row.get(field.name, getattr(self, field.name, None)))
            original_init(self, **{f.name: getattr(self, f.name) for f in fields(cls)})

        cls.__init__ = __init__

        def to_dict(self) -> Dict[str, Any]:
            """
            Convert the dataclass back to a dictionary suitable for writing to a CSV file.
            """
            return {field.name: getattr(self, field.name) for field in fields(self)}
        
        cls.to_dict = to_dict

        cls.is_csv_row = True

        cls.file_path = file_path

        return cls
    return decorator

def is_csv_row(cls: Type[Any]) -> bool:
    """
    Check if a class has been enhanced with the 'csv_row' decorator.
    """
    return hasattr(cls, "is_csv_row") and cls.is_csv_row