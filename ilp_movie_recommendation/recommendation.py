# the model here is the ap andante program

class RecommendationSystem:
    def __init__(self, model):
        self.model = model

    def recommend_movies(self, user_id):
        result, df = self.model.query(f"recommend({user_id}, Movie).")
        if result:
            print(f"Recommendations for {user_id}:")
            print(df)
        else:
            print(f"No recommendations found for {user_id}.")
