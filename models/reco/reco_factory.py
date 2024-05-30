from typing import List
from models.reco.reco_node import RecoNode
from models.reco.reco_rel import RecoRel
import json

class RecoFactory:
    @staticmethod
    def from_file(file_path: str) -> List[List[RecoRel]]:
        with open(file_path, "r") as f:
            return RecoFactory.from_json(f.read())

    @staticmethod
    def from_json(json_str: str) -> List[List[RecoRel]]:
        rows = json.loads(json_str)
        return RecoFactory.from_list(rows)

    @staticmethod
    def from_list(rows: List[List[str]]) -> List[List[RecoRel]]:
        nodes = []
        for row in rows:
            nodes.append(RecoNode(row[1], int(row[2])))
        rels = []
        for i in range(1, len(rows)):
            # if i is even, current -> prev
            if i % 2 == 0:
                rels.append(RecoRel(nodes[i], rows[i][0], nodes[i-1]))
            # if i is odd, prev -> current
            else:
                rels.append(RecoRel(nodes[i-1], rows[i][0], nodes[i]))
        return rels