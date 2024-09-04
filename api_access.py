from fastapi import FastAPI
from typing import List

app = FastAPI()

from pgpr_reco_new_user import extract_recommendation_path

@app.get("/")
# def read_root(pid_list:List[int], gender:str, age:str, k:int=1):
def read_root(pid_list, gender, age, k=1):
	return extract_recommendation_path(pid_list, gender=gender, age=age, number_of_paths=k)
