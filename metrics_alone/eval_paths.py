import os

ROOT_PATH = os.path.abspath(".")
DATA_DIR = os.path.join(ROOT_PATH, "results/")

if not os.path.exists(DATA_DIR):
    ROOT_PATH = os.path.abspath("..")
    DATA_DIR = os.path.join(ROOT_PATH, "results/")
