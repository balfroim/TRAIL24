from dataclasses import dataclass

from models.reco.reco_node import RecoNode


@dataclass
class RecoRel:
    in_node: RecoNode
    relation: str
    out_node: RecoNode