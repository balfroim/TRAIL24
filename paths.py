import os

ROOT_PATH = os.path.abspath(".")
PREPROCESSED_PATH = os.path.join(ROOT_PATH, "results/ml1m/preprocessed")

# Quick fix to allow usage of models in subdirectories (e.g., in notebooks dir)
# TODO need to refactor
if not os.path.exists(PREPROCESSED_PATH):
    ROOT_PATH = os.path.abspath("..")
    PREPROCESSED_PATH = os.path.join(ROOT_PATH, "results/ml1m/preprocessed")

PATHS = {
    "pred_paths": os.path.join(PREPROCESSED_PATH, "pgpr/pred_paths.pkl"),
    "products": os.path.join(PREPROCESSED_PATH, "products.txt"),
    "product_mapping": os.path.join(PREPROCESSED_PATH, "pgpr/mappings/product_mapping.txt"),
    "user_mapping": os.path.join(PREPROCESSED_PATH, "pgpr/mappings/user_mapping.txt"),
    "recommendations": os.path.join(ROOT_PATH, "results/recommendations/"),
    "kg": os.path.join(PREPROCESSED_PATH, "kg_final.txt"),
    "ratings": os.path.join(PREPROCESSED_PATH, "ratings.txt"),
    "users": os.path.join(PREPROCESSED_PATH, "users.txt"),
    "r_map": os.path.join(PREPROCESSED_PATH, "r_map.txt"),
}