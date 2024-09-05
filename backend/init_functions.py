from langchain_community.llms import HuggingFaceEndpoint

# from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from recommendation.explainers.cot_explainer import COTExplainer
from recommendation.explainers.fact_explainer import FactExplainer
from recommendation.explainers.llm_explainer import LLMExplainer

from typing import Any, Dict, List, Optional, Iterator
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk
import requests


def init_cot_explainer(product_registry, user_registry, rating_registry, repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"):

    reasoning_llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        **{
            "max_new_tokens": 1500,
            "temperature": 0.1,
            "top_k": 50,
            "top_p": 0.9,
            "repetition_penalty": 1.1
        },
    )

    answering_llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        **{
            "max_new_tokens": 200,
            "temperature": 0.4,
            "top_k": 30,
            "top_p": 0.8,
            "repetition_penalty": 1.05
        },
    )

    reasoning_template = """You are an expert in graph-based recommender systems.
    You try to follow the following explanation goal:
    1. **Transparency:** Clearly explain how the recommendation algorithm made the decision.
    2. **Scrutability:** Allow the user to provide feedback if the recommendation seems incorrect.
    3. **Trust:** Build user’s confidence in the recommender system.
    4. **Effectiveness:** Help user make informed decisions about the recommendation.
    5. **Efficiency:** Provide a quick explanation to facilitate faster decision-making.
    6. **Persuasiveness:** Convince user of the relevance of the recommendation.
    7. **Satisfaction:** Enhance the ease of use and overall experience of the system for the user.
    Given the background knowledge: {background_knowledge},
    explain why the movie "{product_name}" was recommended to the user {user}.
    """

    reasoning_prompt = PromptTemplate.from_template(reasoning_template)

    answer_template = """Based on the reasoning provided: {reasoning},
    give a concise and helpful response about why the movie "{product_name}" was recommended to the user {user} 
    without repeating the explanation goals.
    """
    answer_prompt = PromptTemplate.from_template(answer_template)

    reasoning_chain = reasoning_prompt | reasoning_llm
    answering_chain = answer_prompt | answering_llm

    cot_explainer = COTExplainer(product_registry, user_registry, rating_registry, reasoning_chain, answering_chain)

    return cot_explainer

ZS_TEMPLATE = """{context}

    Explain to {user} why {product} was recommended to them.
    You can assume that the system is using a simple collaborative filtering approach.
    The explanation should be clear and concise, without any technical jargon.
    It should also be written in a way that is easy to understand for a non-technical user.
    The length should be around 1-2 paragraphs.
    The tone should be friendly and helpful but avoid greeting the user.
    You can use phrases like "we noticed", "we thought", "we hope" to make the explanation more conversational. 
    You can also use phrases like "similar interests", "related product", "many users who liked" to make the explanation more relatable and easy to understand.
    Put your response inside <explanation> for parsing."""

def init_llm_explainer(registry_handler):
        
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        # repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        **{
            "max_new_tokens": 512,
            "top_k": 50,
            "temperature": 0.1,
            "repetition_penalty": 1.03,
        },
    )

    prompt = PromptTemplate.from_template(ZS_TEMPLATE)

    chain = prompt | llm

    return FactExplainer(registry_handler, chain)


def init_llm_explainer_self_hosted(registry_handler):

    class CustomAPIWrapperLLM(LLM):
        """
        A LangChain-compatible LLM that uses a custom FastAPI for text generation.

        This class wraps around a custom FastAPI API and makes HTTP requests
        to generate text using the provided prompt.

        Example:
            .. code-block:: python

                llm = CustomAPIWrapperLLM(api_url="http://localhost:8000")
                result = llm("Tell me a story about a knight")
        """

        api_url: str
        """The URL of the FastAPI server to send requests to."""

        def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
        ) -> str:
            """
            Send a request to the FastAPI server for text generation.

            Args:
                prompt: The prompt to generate from.
                stop: Stop words to use when generating. This example does not implement stop words.
                run_manager: Callback manager for the run.
                **kwargs: Arbitrary additional keyword arguments.

            Returns:
                The generated text from the FastAPI API.
            """
            if stop:
                raise ValueError("Stop words are not implemented in this example.")

            # Send the prompt to the FastAPI server
            response = requests.post(
                f"{self.api_url}/generate",
                json={"text": prompt},
            )

            # Ensure the response is valid
            if response.status_code != 200:
                raise ValueError(f"Error from API: {response.status_code}, {response.text}")

            # Parse and return the generated text
            response_json = response.json()
            return response_json.get("text", "")

        def _stream(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
        ) -> Iterator[GenerationChunk]:
            """
            This method would be used for streaming responses, but it's not implemented
            in this example since FastAPI does not support streaming directly.

            Args:
                prompt: The prompt to generate from.
                stop: Stop words to use when generating (not implemented here).
                run_manager: Callback manager for the run.
                **kwargs: Arbitrary additional keyword arguments.

            Yields:
                Iterator of GenerationChunk with streamed text chunks.
            """
            # Assuming your API does not support streaming, this method can be skipped
            # or you can raise a NotImplementedError if needed.
            raise NotImplementedError("Streaming is not implemented for this API")

        @property
        def _identifying_params(self) -> Dict[str, Any]:
            """Return a dictionary of identifying parameters."""
            return {
                "api_url": self.api_url,
            }

        @property
        def _llm_type(self) -> str:
            """Return the type of LLM."""
            return "custom_api_llm"
        
    llm = CustomAPIWrapperLLM(api_url="http://localhost:28080")

    prompt = PromptTemplate.from_template(ZS_TEMPLATE)

    chain = prompt | llm

    return FactExplainer(registry_handler, chain)