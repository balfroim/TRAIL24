from ast import Tuple
from typing import Union
from attr import dataclass
from dotenv import load_dotenv
from os import getenv
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain.chains.llm import LLMChain
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from numpy import dtype
from dataclasses import dataclass
from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_path import RecoPath
from models.users.user_registry import UserRegistry
from recommendation.explainers.abstract_explainer import AbstractExplainer
from langchain_core.runnables import Runnable
# set a custom Type LLM = Union[
    #     Runnable[LanguageModelInput, str], Runnable[LanguageModelInput, BaseMessage]
    # ]

LLM = Union[
    Runnable[LanguageModelInput, str], Runnable[LanguageModelInput, BaseMessage]
]


@dataclass
class COTTrace:
    reasoning_prompt: str
    reasoning_completion: str
    answering_prompt: str
    answering_completion: str

class COTExplainer(AbstractExplainer):
    def __init__(
            self,
            product_registry: ProductRegistry,
            user_registry: UserRegistry,
            rating_registry: RatingRegistry,
            reasoning_chain: LLMChain,
            answering_chain: LLMChain
    ):
        super().__init__(product_registry, user_registry, rating_registry)
        self.__reasoning_chain = reasoning_chain
        self.__answering_chain = answering_chain

        # self.__llm_chain combine reasoning_chain and answering_chain
        # but with a way to capture the reasoning_chain output
        



        # self.__reasoning_chain = reasoning_prompt | reasoning_llm | StrP
        # self.__answering_chain = LLMChain(prompt=answering_prompt, llm=answering_llm)


        # template = """{background_knowledge}

        # You are a tooltip explaining to {user} why {product_name} was recommended to them in a paragraph."""
        # prompt = PromptTemplate.from_template(template)
        # load_dotenv()
        # llm = HuggingFaceEndpoint(
        #     repo_id=repo_id,
        #     **{
        #         "max_new_tokens": 512,
        #         "top_k": 50,
        #         "temperature": 0.1,
        #         "repetition_penalty": 1.03,
        #         "huggingfacehub_api_token": getenv("HUGGINGFACEHUB_API_TOKEN")
        #     },
        # )
        # self.__llm_chain = LLMChain(prompt=prompt, llm=llm)

    def explain(self, path: RecoPath) -> tuple[str, COTTrace]:
        bk = self.generate_facts(path)
        product_eid = path.recommendation[1].entity_id
        product = self.product_registry.find_by_eid(product_eid)
        user_eid = path.recommendation[0].entity_id
        user = self.user_registry.find_by_eid(user_eid)
        reasoning_completion = self.__reasoning_chain.invoke({
            "background_knowledge": bk,
            "user": str(user),
            "product_name": product.name
        })
        # reasoning_prompt = self.__reasoning_chain.prompt
        print(reasoning_completion)
        answering_completion = self.__answering_chain.invoke({
            "reasoning": reasoning_completion,
            "user": str(user),
            "product_name": product.name
        })
        return answering_completion, COTTrace(
            reasoning_prompt=self.__reasoning_chain.prompt,
            reasoning_completion=reasoning_completion,
            answering_prompt=self.__answering_chain.prompt,
            answering_completion=answering_completion
        )
        # result = self.__llm_chain.invoke({
        #     "background_knowledge": bk,
        #     "user": str(user),
        #     "product_name": product.name
        # })
        # return result["text"]
