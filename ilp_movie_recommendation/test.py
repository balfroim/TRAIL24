from ilp_movie_recommendation.data_processing import Preprocessing

from ilp_movie_recommendation.logic_program_generation import LogicProgramGenerator

from ilp_movie_recommendation.model_generation import ILPModelGenerator


from models.csv_loader import CSVLoader
from models.products.product_registry import ProductRegistry
from models.products.product_mapping_row import ProductMappingRow
from models.products.product_row import ProductRow
from models.users.user_registry import UserRegistry
from models.users.user_mapping_row import UserMappingRow
from models.users.user_row import UserRow
from models.ratings.rating_registry import RatingRegistry
from models.ratings.rating_row import RatingRow

# Load product, user, and rating data
product_registry = ProductRegistry(CSVLoader(ProductRow).read(), CSVLoader(ProductMappingRow).read())
user_registry = UserRegistry(CSVLoader(UserRow).read(), CSVLoader(UserMappingRow).read())
rating_registry = RatingRegistry(CSVLoader(RatingRow).read(), user_registry, product_registry)

#Test preprocessing 
preprocessing = Preprocessing(rating_registry)

# Extract ratings data and convert to DataFrame
ratings_df = preprocessing.extract_ratings_data()

# Save the DataFrame to an Excel file
preprocessing.save_to_excel(ratings_df, "ratings_dataset.xlsx")

# Sample 118 rows and save to another Excel file
preprocessing.sample_and_save(ratings_df, 118, "ratings_sample_dataset.xlsx")

#Test logic programs generation
#Define the file path to your dataset and output directory
file_path = 'ratings_sample_dataset.xlsx'  # Replace with your actual file path
output_dir = './prolog_partitions_six'  # Directory to save the partitions

# Create an instance of the LogicProgramGenerator
logic_program_gen = LogicProgramGenerator(file_path, output_dir)

# Generate balanced partitions and corresponding Prolog logic programs
logic_program_gen.generate_balanced_partitions()


# Define the path to your Prolog file
prolog_file_path = 'prolog_partitions_six/prolog_program_partition_5.pl'
    
# Create an instance of the ILPModelGenerator
ilp_gen = ILPModelGenerator(prolog_file_path)
            
# Generate the model
induced_hypotheses = ilp_gen.generate_model()
print("Induced Hypotheses:")
for clause in induced_hypotheses.clauses:
    print(clause)
            
# Query the model
query = "recommend(A,B)."
result = ilp_gen.query_model(query)
print("\nQuery Result:")