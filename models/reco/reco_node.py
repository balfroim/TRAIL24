from dataclasses import dataclass


@dataclass
class RecoNode:
    type: str
    entity_id: int

    def __str__(self) -> str:
        return f"{self.type.capitalize()}{self.entity_id}"