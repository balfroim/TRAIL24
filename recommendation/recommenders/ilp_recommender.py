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
        "m": "M", 
        "f": "F"
    }

    def __init__(self, product_registry: ProductRegistry, user_registry: UserRegistry, rating_registry: RatingRegistry, seed=42):
        super().__init__(product_registry, user_registry, rating_registry)
        clauses_path = "./ilp_movie_recommendation/combined_rules.txt"
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
        already_watched = [r.product.pid for r in self.rating_registry.find_user_ratings(int(new_user_id))]
        recomm = {}
        for product in self.product_registry.products[:25]:
            nodes = [RecoNode('user', target_user.eid), RecoNode('product', product.eid)]
            rels = []
            cnt = 0
            for clause in self.clauses:
                possible_rel = []
                fit_rule = True
                for u_c in clause['user']:
                    fit_rule = fit_rule and u_c in user_char
                    if fit_rule: possible_rel.append(RecoRel(RecoNode('user', target_user.eid), u_c, RecoNode('user', target_user.eid)))
                fit_rule = fit_rule and product.genre in clause['product']
                if fit_rule: possible_rel.append(RecoRel(RecoNode('product', product.eid), product.genre, RecoNode('product', product.eid)))
                if fit_rule and product.pid not in already_watched:
                    cnt += 1
                    rels += possible_rel
            if cnt != 0:
                recomm[product.eid] = [RecoPath(nodes, rels), cnt]
        sorted_keys = [k for k, v in sorted(recomm.items(), key=lambda item: item[1][1])]
        results = []
        for key in sorted_keys[-1:]:
            results.append(recomm[key][0])
        return results

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
    new_user = User(0, 1, 'M', '56+')
    rec.recommend(new_user)