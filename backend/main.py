from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
# from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from models.csv_loader import CSVLoader
from models.products.product_mapping_row import ProductMappingRow
from models.products.product_registry import ProductRegistry
from models.products.product_row import ProductRow
from models.ratings.rating import Rating
from models.ratings.rating_registry import RatingRegistry
from models.ratings.rating_row import RatingRow
from models.users.user import User
from models.users.user_mapping_row import UserMappingRow
from models.users.user_registry import UserRegistry
from models.users.user_row import UserRow
from recommendation.explainers.cot_explainer import COTExplainer
from recommendation.recommenders.random_recommender import RandomRecommender

product_registry = ProductRegistry(CSVLoader(ProductRow).read(), CSVLoader(ProductMappingRow).read())
user_registry = UserRegistry(CSVLoader(UserRow).read(), CSVLoader(UserMappingRow).read())
rating_registry = RatingRegistry(CSVLoader(RatingRow).read(), user_registry, product_registry)

recommender = RandomRecommender(product_registry, user_registry, rating_registry)

repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

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

# TODO cache recommendation paths to generate explanations
user_reco_path_dict = {}

# data structure for product search
name_pid_tuples = [
    (product.name.lower().strip(), product.pid)
    for product in product_registry.products
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProfileSchema(BaseModel):
    gender_cat: str
    age_cat: str

class RatingSchema(BaseModel):
    product_id: int
    value: float

class QuerySchema(BaseModel):
    value: str

# TODO to implement
@app.get("/")
def serve_front():
    return {"Serve": "Front"}

# TODO deal with no user_id case (it must be returned by the backend)

@app.post("/set_profile")
def set_profile(profile: ProfileSchema):
    user_data = User(eid=0, uid=0, gender=profile.gender_cat, age=profile.age_cat)
    user = user_registry.add_user(user_data)

    return user.uid

@app.post("/search")
def search_products(query: QuerySchema):
    formatted_value = query.value.lower().strip()

    if not formatted_value:
        return {}

    results = [t for t in name_pid_tuples if formatted_value in t[0]]

    return {t[1]: t[0] for t in results}

@app.post("/rate/{user_id}")
def rate_product(user_id: int, rating: RatingSchema):
    user = user_registry.find_by_uid(user_id)
    product = product_registry.find_by_pid(rating.product_id)

    rating = Rating(user, product, rating.value)
    rating_registry.add_rating(rating)

    return Response(status_code=status.HTTP_200_OK)

@app.delete("/rate/{user_id}/{product_id}")
def delete_rating(user_id: int, product_id: int):
    rating_registry.delete_rating(user_id, product_id)

    return Response(status_code=status.HTTP_200_OK)

@app.get("/rec/{user_id}")
async def get_recommendation(user_id: int):
    user = user_registry.find_by_uid(user_id)
    reco_paths = recommender.recommend(user, 9)
    recommendations = {}
    products = []
    for reco_path in reco_paths:
        reco_product = product_registry.find_by_eid(reco_path.nodes[-1].entity_id)
        products.append(reco_product)
        recommendations[reco_product.pid] = reco_path
    user_reco_path_dict[user_id] = recommendations

    return [
        {
            "pid": product.pid,
            "name": product.name,
            "genre": product.genre
        }
        for product in products
    ]

@app.get("/explain/{user_id}/{product_id}")
async def get_explanation(user_id: int, product_id: int):
    reco_path = user_reco_path_dict[user_id][product_id]
    explanation = cot_explainer.explain(reco_path)

    return explanation
