from dotenv import load_dotenv
from os import getenv
from langchain.chains.llm import LLMChain
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user_registry import UserRegistry
from recommendation.explainers.abstract_explainer import AbstractExplainer


class LLMExplainer(AbstractExplainer):
    def __init__(
            self,
            product_registry: ProductRegistry,
            user_registry: UserRegistry,
            rating_registry: RatingRegistry,
            repo_id: str
    ):
        super().__init__(product_registry, user_registry, rating_registry)
        template = """{background_knowledge}

        You are a tooltip explaining to {user} why {product_name} was recommended to them in a paragraph."""
        prompt = PromptTemplate.from_template(template)
        load_dotenv()
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            **{
                "max_new_tokens": 512,
                "top_k": 50,
                "temperature": 0.1,
                "repetition_penalty": 1.03,
                "huggingfacehub_api_token": getenv("HUGGINGFACEHUB_API_TOKEN")
            },
        )
        self.__llm_chain = LLMChain(prompt=prompt, llm=llm)

    def explain(self, path: RecoPath) -> str:
        bk = self.generate_facts(path)
        product_eid = path.recommendation[1].entity_id
        product = self.product_registry.find_by_eid(product_eid)
        user_eid = path.recommendation[0].entity_id
        user = self.user_registry.find_by_eid(user_eid)
        result = self.__llm_chain.invoke({
            "background_knowledge": bk,
            "user": str(user),
            "product_name": product.name
        })
        return result["text"]
