from dataclasses import dataclass


@dataclass
class RecoNode:
    type: str
    entity_id: int