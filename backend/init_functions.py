from langchain_community.llms import HuggingFaceEndpoint
# from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

from recommendation.explainers.cot_explainer import COTExplainer

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