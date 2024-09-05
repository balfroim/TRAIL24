from data_processing import Preprocessing

from logic_program_generation import LogicProgramGenerator

from model_generation import ILPModelGenerator


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
print("preprocessed")

# Extract ratings data and convert to DataFrame
ratings_df = preprocessing.extract_ratings_data()
print("extracted")

# Sample 118 rows and save to another Excel file
preprocessing.sample_and_save(ratings_df, 118, "/ilp_movie_recommendation/ratings_sample_dataset.xlsx")
print("sampled")

#Test logic programs generation
#Define the file path to your dataset and output directory
file_path = 'ratings_sample_dataset.xlsx'  # Replace with your actual file path
output_dir = './prolog_partitions_six'  # Directory to save the partitions

# Create an instance of the LogicProgramGenerator
logic_program_gen = LogicProgramGenerator(file_path, output_dir)
print('program generator')

# Generate balanced partitions and corresponding Prolog logic programs
logic_program_gen.generate_balanced_partitions()
print("balanced partitions")


# Define the path to your Prolog file
prolog_file_path = 'prolog_partitions_six/prolog_program_partition_5.pl'
    
# Create an instance of the ILPModelGenerator
ilp_gen = ILPModelGenerator(prolog_file_path)
print('model generator')
            
# Generate the model
induced_hypotheses = ilp_gen.generate_model()
print("Induced Hypotheses:")
lines = []
for clause in induced_hypotheses.clauses:
    print(clause)
    lines.append(str(clause)+"\n")
with open("ilp_movie_recommendation/learned_clauses.txt", 'w') as f:
    f.writelines(lines)

# Query the model
query = "recommend(A,B)."
result = ilp_gen.query_model(query)
print("\nQuery Result:", result)

from andante.program import AndanteProgram# Chemin vers le fichier Prolog
file_path = 'prolog_partitions_six/prolog_program_partition_5.pl'# Ajouter un nouvel utilisateur au programme
new_user_id = "u777"
new_user_age = "b25to34"  # Groupe d'âge: 25-34
new_user_gender = "m"  # Sexe: Masculin
new_movie_id = "m777"
user_movie_genre = "action"
rating_movie = add_new_user_to_existing_program(file_path, new_user_id, new_user_age, new_user_gender, new_movie_id, user_movie_genre, rating_movie)# Charger le programme Prolog avec les nouvelles données
ap = AndanteProgram.build_from(file_path)# Définir les paramètres pour l'inférence
ap.set('verbose', 1)
ap.set('h', 100)# Générer les règles si elles ne sont pas déjà générées
induced_rules = ap.induce(update_knowledge=True, logging=True, verbose=0)# Recommander un film pour le nouvel utilisateur
result, df = ap.query(f"recommend({new_user_id}, Movie).")# Afficher les recommandations
if result:
    print(f"Recommandations pour {new_user_id}:")
    print(df)
else:
    print(f"Aucune recommandation trouvée pour {new_user_id}.")