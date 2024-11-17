import json
import os

from data_access.validation_helper import validate_json
from models.autorisation import Autorisation
from models.troc import Troc

DATA_FOLDER_AUTORIZATION = "data/autorisations/"

def get_autorization_by_id_fichier(id_fichier) -> Autorisation:
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
        """
    is_valid = validate_json(id_fichier, "schema/schema_autorisation.json")
    file = open(id_fichier, encoding="utf-8")
    json_data = json.load(file)
    return Autorisation.from_json(json_data)


def get_all_autorizations(folder_path=DATA_FOLDER_AUTORIZATION):
    autorizations = []
    for file in os.listdir(folder_path):
        # check the files which are end with specific extension
        if file.endswith(".json"):
            # print path name of selected files
            try:
                # retenir quelque part le nom du fichier
                autorizations.append(get_autorization_by_id_fichier(os.path.join(folder_path, file)))
            except Exception as e:
                print(f"erreur dans le fichier {e}")
    return autorizations

    pass

def filter_autorization_by_id_troqueur_id_destinateur_id_fichier(id_troqueur, id_destinateur, id_fichier) -> Troc:
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
        """
    all_auto = get_all_autorizations()
    for auto in all_auto:
        if auto.id_troqueur == id_troqueur and auto.id_destinataire == id_destinateur and auto.id_fichier == id_fichier:
            return auto
    return None








