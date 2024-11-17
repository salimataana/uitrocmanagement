import json
import os

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
            except Exception as e:
                trocs_malformated.append(file),
                print(f"erreur dans le fichier {e}")
    return trocs_malformated

def get_all_trocs(folder_path):
    malformatted_files =  get_all_trocs_malformated(folder_path)
    well_formated_files = get_all_trocs_well_formatted(folder_path)
    return well_formated_files, malformatted_files

