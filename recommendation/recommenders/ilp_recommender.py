import random
from typing import List

from models.products.product_registry import ProductRegistry
from models.ratings.rating_registry import RatingRegistry
from models.reco.reco_node import RecoNode
from models.reco.reco_path import RecoPath
from models.reco.reco_rel import RecoRel
from models.users.user import User
from models.users.user_registry import UserRegistry
from recommendation.recommenders.abstract_recommender import AbstractRecommender

from andante.program import AndanteProgram
import numpy as np


class ILPRecommender(AbstractRecommender):
    """
    Generates ILP recommendations for a target user.
    """
    
    clauses = None
    
    clauses_dic = {
        "under_18": "Under 18",
        "b18to24": "18-24",
        "b25to34": "25-34",
        "b35to44": "35-44",
        "b45to49": "45-49",
        "b50to55": "50-55",
        "plus56": "56+",
        "action": "Action",
        "adventure": "Adventure",
        "animation": "Animation",
        "childrens": "Children's",
        "comedy": "Comedy",
        "crime": "Crime",
        "documentary": "Documentary",
        "drama": "Drama",
        "fantasy": "Fantasy",
        "filmnoir": "Film-Noir",
        "horror": "Horror",
        "musical": "Musical",
        "mystery": "Mystery",
        "romance": "Romance",
        "sci_fi": "Sci-Fi",
        "thriller": "Thriller",
        "western": "Western",
        "war": "War",
        "m": "m", 
        "f": "f"
    }

    def __init__(self, product_registry: ProductRegistry, user_registry: UserRegistry, rating_registry: RatingRegistry, seed=42):
        super().__init__(product_registry, user_registry, rating_registry)
        clauses_path = "./ilp_movie_recommendation/learned_clauses.txt"
        rules = []
        with open(clauses_path, 'r') as f:
            for line in f.readlines():
                rule = line.split(' :- ')[-1].strip()
                atoms = rule[:-1].split(', ')
                conditions = {'user': [], 'product': []}
                for atom in atoms:
                    if '(A,B)' in atom:
                        print("todo, handle atoms on both user and product")
                    elif '(A)' in atom:
                        conditions["user"].append(self.clauses_dic[atom[:-3]])
                    elif '(B)' in atom:
                        conditions["product"].append(self.clauses_dic[atom[:-3]])
                    else:
                        print('unrecognized atom:', atom)
                rules.append(conditions)
        print('rules', rules)
        self.clauses = rules

    def recommend(self, target_user: User) -> List[RecoPath]:
        new_user_id = str(target_user.uid)
        new_user_age = str(target_user.age)
        new_user_gender = target_user.gender
        user_char = [new_user_id, new_user_age, new_user_gender]
        recomm = {}
        for product in self.product_registry.products:
            nodes = []
            rels = []
            for clause in self.clauses:
                if clause['user'] in user_char or product.genre in clause['product']:
                    nodes.append(RecoNode())
            recomm[product.eid] = cnt_match
        
                
        """ # TODO This process need some optimization... ^^
        #1: gather target_user's ratings
        user_ratings = self.rating_registry.find_user_ratings(target_user.uid)
        user_product_pid_set = { rating.product.pid for rating in user_ratings }

        #2: gather other users' ratings of products rated by target_user
        partial_rating_paths = []
        for user_rating in user_ratings:
            product = user_rating.product
            related_ratings = [rating for rating in self.rating_registry.find_product_ratings(product.pid)]
            # remove target_user's ratings
            related_ratings = filter(lambda rating: rating.user.uid != target_user.uid, related_ratings)
            for related_rating in related_ratings:
                partial_rating_paths.append([user_rating, related_rating])

        #3: gather product ratings by other related users
        complete_rating_paths = []
        for partial_rating_path in partial_rating_paths:
            same_product_rating = partial_rating_path[-1]
            related_user_ratings = self.rating_registry.find_user_ratings(same_product_rating.user.uid)
            # remove ratings of products already rated by target_user
            related_user_ratings = filter(lambda rating: rating.product.pid not in user_product_pid_set, related_user_ratings)
            for related_user_rating in related_user_ratings:
                complete_rating_paths.append([*partial_rating_path, related_user_rating])

        #4: select one at random
        recommended_rating_path = random.choice(complete_rating_paths)

        #5: build reco path
        #TODO need to extract this code in another place (SRP)
        reco_path = RecoPath([], [])
        for rating in recommended_rating_path:
            reco_user_node = RecoNode("user", rating.user.eid)
            reco_product_node = RecoNode("product", rating.product.eid)
            reco_path.nodes.append(reco_user_node)
            reco_path.nodes.append(reco_product_node)
            reco_rel = RecoRel(reco_user_node, "watched", reco_product_node)
            reco_path.rels.append(reco_rel)

        #TODO return more than a single recommendation
        return [reco_path] """

if __name__ == "__main__":
    from models.csv_loader import CSVLoader
    from models.products.product_registry import ProductRegistry
    from models.products.product_mapping_row import ProductMappingRow
    from models.products.product_row import ProductRow
    product_registry = ProductRegistry(CSVLoader(ProductRow).read(), CSVLoader(ProductMappingRow).read())
    from models.users.user_registry import UserRegistry
    from models.users.user_mapping_row import UserMappingRow
    from models.users.user_row import UserRow
    user_registry = UserRegistry(CSVLoader(UserRow).read(), CSVLoader(UserMappingRow).read())
    from models.ratings.rating_registry import RatingRegistry
    from models.ratings.rating_row import RatingRow
    rating_registry = RatingRegistry(CSVLoader(RatingRow).read(), user_registry, product_registry)
    
    rec = ILPRecommender(product_registry, user_registry, rating_registry)
    new_user = User(0, 0, 'm', '56+')
    rec.recommend(new_user)