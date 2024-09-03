import pandas as pd
import os

class LogicProgramGenerator:
    def __init__(self, file_path, output_dir):
        self.file_path = file_path
        self.output_dir = output_dir

    def generate_balanced_partitions(self):
        # Load the dataset
        data = pd.read_excel(self.file_path)

        # Define all possible categories for age, genres, and gender
        possible_ages = {
            "Under 18": "under_18",
            "18-24": "b18to24",
            "25-34": "b25to34",
            "35-44": "b35to44",
            "45-49": "b45to49",
            "50-55": "b50to55",
            "56+": "plus56"
        }
        
        possible_genres = {
            "Action": "action",
            "Adventure": "adventure",
            "Animation": "animation",
            "Children's": "childrens",
            "Comedy": "comedy",
            "Crime": "crime",
            "Documentary": "documentary",
            "Drama": "drama",
            "Fantasy": "fantasy",
            "Film-Noir": "filmnoir",
            "Horror": "horror",
            "Musical": "musical",
            "Mystery": "mystery",
            "Romance": "romance",
            "Sci-Fi": "sci_fi",
            "Thriller": "thriller",
            "Western": "western",
            "War": "war"
        }

        possible_genders = ["m", "f"]

        # Split the data into positive and negative examples
        positive_data = data[data['rating'] > 3].copy()
        negative_data = data[data['rating'] <= 3].copy()

        # Shuffle the data
        positive_data = positive_data.sample(frac=1, random_state=42).reset_index(drop=True)
        negative_data = negative_data.sample(frac=1, random_state=42).reset_index(drop=True)

        # Determine the size of each partition
        num_partitions = 6
        pos_partition_size = len(positive_data) // num_partitions
        neg_partition_size = len(negative_data) // num_partitions

        # Ensure that the partitions are balanced
        partitions = []
        for i in range(num_partitions):
            pos_start = i * pos_partition_size
            pos_end = pos_start + pos_partition_size
            neg_start = i * neg_partition_size
            neg_end = neg_start + neg_partition_size

            # Handle remainders by distributing them to the partitions
            if i == num_partitions - 1:
                pos_end = len(positive_data)
                neg_end = len(negative_data)

            partition = pd.concat([
                positive_data.iloc[pos_start:pos_end],
                negative_data.iloc[neg_start:neg_end]
            ]).reset_index(drop=True)
            
            partitions.append(partition)

        # Generate Prolog programs for each partition
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        for i, partition in enumerate(partitions):
            output_file_name = f"{self.output_dir}/prolog_program_partition_{i+1}"
            self.generate_progol_program_for_partition(partition, possible_ages, possible_genres, possible_genders, output_file_name)

    def generate_progol_program_for_partition(self, partition, possible_ages, possible_genres, possible_genders, output_file_name):
        # Prepare containers for Prolog facts
        positive_examples = []
        negative_examples = []
        background_knowledge = set()

        # Track the present predicates
        present_ages = set()
        present_genres = set()
        present_genders = set()

        # Process each row in the partition
        for _, row in partition.iterrows():
            user_id = f"u{row['userid']}"
            movie_id = f"m{row['productid']}"
            rating = row['rating']
            age_group = possible_ages.get(row['age'], "").lower()  # Replace age group with corresponding Prolog predicate
            gender = row['gender'].lower()  # Normalize gender
            genre = possible_genres.get(row['pgenre'], "").lower()  # Replace genre with corresponding Prolog predicate

            # Generate positive and negative examples
            if rating > 3:
                positive_examples.append(f"recommend({user_id}, {movie_id}).")
            else:
                negative_examples.append(f"recommend({user_id}, {movie_id}).")

            # Background knowledge: user attributes
            if age_group:
                background_knowledge.add(f"{age_group}({user_id}).")
                present_ages.add(age_group)
            if gender in possible_genders:
                background_knowledge.add(f"{gender}({user_id}).")
                present_genders.add(gender)

            # Background knowledge: movie genre
            if genre:
                background_knowledge.add(f"{genre}({movie_id}).")
                present_genres.add(genre)

        # Mode declarations
        modeh_declaration = "modeh(*, recommend(+user, +movie))."
        modeb_declarations = [
            f"modeb(*, {age}(+user))." for age in present_ages
        ] + [
            f"modeb(*, {gender}(+user))." for gender in present_genders
        ] + [
            f"modeb(*, {genre}(+movie))." for genre in present_genres
        ]
        modeb_declarations = [declaration for declaration in modeb_declarations if declaration]  # Remove empty strings

        # Determinations
        determinations = [
            f"determination(recommend/2, {age}/1)." for age in present_ages
        ] + [
            f"determination(recommend/2, {gender}/1)." for gender in present_genders
        ] + [
            f"determination(recommend/2, {genre}/1)." for genre in present_genres
        ]
        determinations = [determination for determination in determinations if determination]  # Remove empty strings

        # Combine all parts into a Progol-compatible logic program
        progol_program = "% Mode Declarations\n"
        progol_program += modeh_declaration + "\n"
        progol_program += "\n".join(modeb_declarations) + "\n\n"

        progol_program += "% Determinations\n"
        progol_program += "\n".join(determinations) + "\n\n"

        progol_program += "% Background Knowledge\n:- begin_bg.\n"
        progol_program += "\n".join(sorted(background_knowledge)) + "\n:- end_bg.\n\n"

        progol_program += "% Positive Examples\n:- begin_in_pos.\n"
        progol_program += "\n".join(positive_examples) + "\n:- end_in_pos.\n\n"

        progol_program += "% Negative Examples\n:- begin_in_neg.\n"
        progol_program += "\n".join(negative_examples) + "\n:- end_in_neg.\n"

        # Save the Progol logic program to a file with a custom name
        output_file_path = f"{output_file_name}.pl"
        with open(output_file_path, "w") as file:
            file.write(progol_program)

        print(f"Progol logic program saved as {output_file_path}")
