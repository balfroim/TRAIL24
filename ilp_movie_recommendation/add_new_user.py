def add_new_user_to_existing_program(file_path, new_user_id, new_user_age, new_user_gender, new_movie_id, user_movie_genre, rating_movie):
    # Lire le fichier existant
    with open(file_path, 'r') as file:
        lines = file.readlines()    # Vérifier si l'utilisateur existe déjà dans le fichier
    user_exists = any(f"{new_user_id}" in line for line in lines)   
    if user_exists:
        print(f"L'utilisateur {new_user_id} existe déjà dans le programme.")
        return    # Variables pour garder les lignes modifiées
    new_lines = []
    bg_inserted = False
    pos_inserted = False
    neg_inserted = False    
    for line in lines:
        # Ajouter les nouvelles données dans la bonne section
        if ":- end_bg." in line and not bg_inserted:
            # Ajouter les nouvelles données de background knowledge avant la fin de la section bg
            new_lines.append(f"{new_user_age}({new_user_id}).\n")
            new_lines.append(f"{new_user_gender}({new_user_id}).\n")
            new_lines.append(f"{user_movie_genre}({new_movie_id}).\n")
            bg_inserted = True        
            if ":- end_in_pos." in line and not pos_inserted and rating_movie > 3:
                # Ajouter la recommandation positive si le rating est > 3 avant la fin de la section pos
                new_lines.append(f"recommend({new_user_id}, {new_movie_id}).\n")
                pos_inserted = True        
            if ":- end_in_neg." in line and not neg_inserted and rating_movie <= 3:
                # Ajouter la recommandation négative si le rating est <= 3 avant la fin de la section neg
                new_lines.append(f"recommend({new_user_id}, {new_movie_id}).\n")
                neg_inserted = True        # Ajouter la ligne originale
        new_lines.append(line)    # Sauvegarder les modifications dans le fichier
    with open(file_path, 'w') as file:
        file.writelines(new_lines)    
        print(f"Le programme logique a été mis à jour et sauvegardé dans {file_path}")