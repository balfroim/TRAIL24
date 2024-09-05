from datetime import datetime

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.init_functions import init_cot_explainer, init_llm_explainer, init_llm_explainer_self_hosted
from backend.metadata_functions import get_poster_path_from_pid, get_abstract_from_pid
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
from recommendation.recommenders.personalized_pagerank_recommender import PersonalizedPageRankRecommender
from recommendation.recommenders.random_recommender import RandomRecommender
import dotenv
from recommendation.registry_handler import RegistryHandler
from recommendation.explainers.llm_explainer import LLMExplainer
from models.reco.reco_factory import RecoFactory
import os 
from paths import PATHS



dotenv.load_dotenv()


product_registry = ProductRegistry(CSVLoader(ProductRow).read(), CSVLoader(ProductMappingRow).read())
user_registry = UserRegistry(CSVLoader(UserRow).read(), CSVLoader(UserMappingRow).read())
rating_registry = RatingRegistry(CSVLoader(RatingRow).read(), user_registry, product_registry)

registry_handler = RegistryHandler(product_registry, user_registry, rating_registry)

recommender = RandomRecommender(product_registry, user_registry, rating_registry)
# recommender = PersonalizedPageRankRecommender(product_registry, user_registry, rating_registry)

# explainer = LLMExplainer(registry_handler, chain)
explainer = init_llm_explainer(registry_handler)
# explainer = init_llm_explainer_self_hosted(registry_handler)
# explainer = init_cot_explainer(product_registry, user_registry, rating_registry)

# load recommendations paths
user_recos = dict()
for json_file_name in os.listdir(PATHS["recommendations"]):
    user_id = int(json_file_name.split("_")[-1].split(".")[0])
    user_reco_path = os.path.join(PATHS["recommendations"], json_file_name)
    user_recos[user_id] = RecoFactory.from_file(user_reco_path)

# data structure for product search
name_pid_tuples = [
    (product.name.lower().strip(), product.pid)
    for product in product_registry.products
]

app = FastAPI()

app.mount('/assets', StaticFiles(directory='frontend/dist/assets'), name='assets')

if not os.getenv("PROD"):
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
    return FileResponse('./Frontend/dist/index.html')

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
    timestamp = int(datetime.timestamp(datetime.now()))
    rating = Rating(user, product, rating.value, timestamp)
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
    user_recos[user_id] = recommendations

    return [
        {
            "pid": product.pid,
            "name": product.name,
            "genre": product.genre
        }
        for product in products
    ]


import re

def extract_explanation(text):
    """
    Extracts the content between <explanation> and </explanation> tags using regular expressions.

    Args:
        text (str): The input text containing <explanation> and </explanation> tags.

    Returns:
        str: The text between <explanation> and </explanation>, or an empty string if not found.
    """
    pattern = r"(?<=<explanation>)(.|\n)*(?=<\/explanation>)"
    match = re.search(pattern, text)

    if match:
        return match.group(0).strip()
       
    return ""

@app.get("/explain/{user_id}/{reco_id}")
async def get_explanations(user_id: int, reco_id: int):
    reco_path = user_recos[user_id][reco_id]
    explanation_with_names, _ = explainer.explain(reco_path)
    explanation_without_names, _ = explainer.explain(reco_path, exclude_predicates=["name"])
    explanation_with_names = extract_explanation(explanation_with_names)
    explanation_without_names = extract_explanation(explanation_without_names)
    return [explanation_with_names, explanation_without_names]

@app.get("/poster/{product_id}")
async def get_poster(product_id: int):
    path = get_poster_path_from_pid(product_id)
    return FileResponse(path)

@app.get("/abstract/{product_id}")
async def get_abstract(product_id: int):
    return get_abstract_from_pid(product_id)
