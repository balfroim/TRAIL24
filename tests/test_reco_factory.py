from models.reco.reco_factory import RecoFactory
from models.reco.reco_node import RecoNode
from models.reco.reco_rel import RecoRel
import pytest

class TestRecoFactory:
    def test_from_file(self):
        pass

    def test_from_json(self):
        pass

    def test_from_list(self):
        lst = [["self_loop", "user", 6], ["watched", "product", 2389], ["watched", "user", 999], ["watched", "product", 2386]]
        reco_rels = RecoFactory.from_list(lst)
        user6 = RecoNode("user", 6)
        product2389 = RecoNode("product", 2389)
        user999 = RecoNode("user", 999)
        product2386 = RecoNode("product", 2386)
        assert reco_rels[0] == RecoRel(user6, "watched", product2389)
        assert reco_rels[1] == RecoRel(user999, "watched", product2389)
        assert reco_rels[2] == RecoRel(user999, "watched", product2386)

