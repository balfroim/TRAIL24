from abc import ABC, abstractmethod
from ast import Not
from typing import List, Optional

from attr import dataclass
from regex import F

from models.nodes.fact import Fact
from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users import user
from models.users.user_registry import UserRegistry
from recommendation.facts.fact_collector import FactCollector
from recommendation.registry_handler import RegistryHandler


# @dataclass
# class Context:
#     user: str
#     product: str
#     background_knowledge: str

class AbstractExplainer(ABC):
    """
    Base class for all explainer methods.
    """

    @abstractmethod
    def __init__(self, registry_handler: RegistryHandler):
        self.registry_handler = registry_handler
        # self.fact_collector = FactCollector(registry_handler)
        
    @abstractmethod
    def _preprocess(self, **kwargs) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    def _process(self, input: dict, **kwargs) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def _postprocess(self, completion: str, **kwargs) -> str:
        raise NotImplementedError

    def explain(self, **kwargs) -> str:
        context = self._preprocess(**kwargs)
        completion = self._process(context, **kwargs)
        return self._postprocess(completion, **kwargs)
    
    
    

        
    
    
