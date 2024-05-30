from io import StringIO
from models.reco.reco_factory import RecoFactory
from models.reco.reco_node import RecoNode
from models.reco.reco_rel import RecoRel
import pytest
from unittest.mock import mock_open, patch

class TestRecoFactory:
    
    @patch('models.reco.reco_factory.open', new_callable=mock_open)
    def test_from_file(self, mock_open_file):
        mock_open_file.side_effect = [StringIO('[["self_loop", "user", 6], ["watched", "product", 2389], ["watched", "user", 999], ["watched", "product", 2386]]')]
        reco_rels = RecoFactory.from_file("file_path")
        user6 = RecoNode("user", 6)
        product2389 = RecoNode("product", 2389)
        user999 = RecoNode("user", 999)
        product2386 = RecoNode("product", 2386)
        assert reco_rels[0] == RecoRel(user6, "watched", product2389)
        assert reco_rels[1] == RecoRel(user999, "watched", product2389)
        assert reco_rels[2] == RecoRel(user999, "watched", product2386)

    def test_to_facts(self):
        # Arrange
        rel = RecoRel(RecoNode("user", 6), "watched", RecoNode("product", 2389))
        # Act
        facts = rel.to_facts()
        # Assert
        assert facts == """watched(User6, Product2389)"""

