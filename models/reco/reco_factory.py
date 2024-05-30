from typing import List

from regex import R
from models.reco.reco_node import RecoNode
from models.reco.reco_path import RecoPath
from models.reco.reco_rel import RecoRel
import json


class RecoFactory:
    @staticmethod
    def from_file(file_path: str) -> List[RecoPath]:
        with open(file_path, "r") as f:
            return RecoFactory.from_json(f.read())

    @staticmethod
    def from_json(json_str: str) -> List[RecoPath]:
        try:
            json_data = json.loads(json_str)
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Invalid JSON: {json_str}")
        return [
            RecoFactory.from_list(path)
            for path in json_data
        ]

    @staticmethod
    def from_list(path: List[List[str]]) -> RecoPath:
        nodes = []
        for raw_node in path:
            nodes.append(RecoNode(raw_node[1], int(raw_node[2])))
        rels = []
        for i in range(1, len(path)):
            # if i is even, current -> prev
            if i % 2 == 0:
                rels.append(RecoRel(nodes[i], path[i][0], nodes[i-1]))
            # if i is odd, prev -> current
            else:
                rels.append(RecoRel(nodes[i-1], path[i][0], nodes[i]))
        return RecoPath(nodes, rels)