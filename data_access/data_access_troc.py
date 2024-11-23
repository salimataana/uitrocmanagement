import json
import os

from flask_login import current_user

from data_access.validation_helper import validate_json
from models.troc import Troc


def get_troc_by_id_fichier(id_fichier) -> Troc:
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
        """
    is_valid = validate_json(id_fichier, "schema/schema_troc.json")
    file = open(id_fichier, encoding="utf-8")
    json_data = json.load(file)
    return Troc.from_json(json_data)

def get_all_trocs_well_formatted(folder_path):
    list_trocs=[]
    for file in os.listdir(folder_path):
        # check the files which are end with specific extension
        if file.endswith(".json"):
            # print path name of selected files
            try:
                #retenir quelque part le nom du fichier
                list_trocs.append(get_troc_by_id_fichier(os.path.join(folder_path, file)))
            except Exception as e:
                print(f"erreur dans le fichier {e}")
    return list_trocs


def get_all_trocs_malformated(folder_path):
    trocs_malformated = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            try:
                print("File well formated")
                get_troc_by_id_fichier(file)
            except Exception as e:
                trocs_malformated.append(os.path.join(folder_path, file)),
                print(f"erreur dans le fichier {e}")
    return trocs_malformated

def get_all_trocs(folder_path):
    malformatted_files =  get_all_trocs_malformated(folder_path)
    well_formated_files = get_all_trocs_well_formatted(folder_path)
    print(malformatted_files)
    return well_formated_files, malformatted_files


def get_all_trocs_sent_by_current_user(folder_path, id_troqueur):
    malformatted_files =  get_all_trocs_malformated(folder_path)
    well_formated_files = get_all_trocs_well_formatted(folder_path)
    well_formated_files=[item for item in well_formated_files if str(item.id_troqueur)==str(id_troqueur) ]
    return  well_formated_files, malformatted_files


def get_all_trocs_received_by_current_user(folder_path, id_troqueur):
    malformatted_files =  get_all_trocs_malformated(folder_path)
    well_formated_files = get_all_trocs_well_formatted(folder_path)
    print(malformatted_files)
    return [item for item in well_formated_files if str(item.id_troqueur)!=str(id_troqueur) ], malformatted_files




def apply_control(file_name):
    # check file size
    file_stats = os.stat(file_name)
    size_file_bytes = file_stats.st_size / 1000
    if size_file_bytes > 2:
        print(f"{file_name} est rejété car sa taille est de {size_file_bytes} > 2")
    # validate_schema
    validate_json(file_path=file_name, validation_schema="")
    print(" Schema validé")
    file = open(file_name, encoding="utf-8")
    json_data = json.load(file)

    troc = Troc.from_json(json_data)

    nbr_message = len(troc.messages)
    # check nombre de messages
    if nbr_message != troc.nombre_messages:
        print("Fichier non valide est rejeté car nombre message different")