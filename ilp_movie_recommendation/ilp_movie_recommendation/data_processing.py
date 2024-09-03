import pandas as pd

class Preprocessing:
    def __init__(self, rating_registry):
        self.rating_registry = rating_registry

    def extract_ratings_data(self):
        """Extracts attributes from the Rating objects and converts them to a DataFrame."""
        ratings_data = [
            {
                "userid": rating.user.uid,
                "gender": rating.user.gender,
                "age": rating.user.age,
                "productid": rating.product.pid,
                "pname": rating.product.name,
                "pgenre": rating.product.genre,
                "rating": rating.rating,
                "timestamp": rating.timestamp
            }
            for rating in self.rating_registry.ratings
        ]
        ratings_df = pd.DataFrame(ratings_data)
        return ratings_df

    def save_to_excel(self, dataframe, output_file):
        """Saves the DataFrame to an Excel file."""
        dataframe.to_excel(output_file, index=False)
        print(f"Dataset successfully saved to {output_file}")

    def sample_and_save(self, dataframe, sample_size, output_file):
        """Takes a sample of the DataFrame and saves it to an Excel file."""
        sample_df = dataframe.sample(n=sample_size, random_state=42)
        sample_df.to_excel(output_file, index=False)
        print(f"Sample dataset successfully saved to {output_file}")
