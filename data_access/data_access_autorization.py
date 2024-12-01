import json
import os

from data_access.validation_helper import validate_json
from models.autorisation import Autorisation
from models.troc import Troc

DATA_FOLDER_AUTORIZATION = "data/demandeautorizationrecu"

def get_autorization_by_id_fichier(id_fichier) -> Autorisation:
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
        """
    #is_valid = validate_json(id_fichier, "schema/schema_autorisation.json")
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

def filter_autorization_by_id_troqueur_id_destinateur_id_fichier(idTroqueur, idDestinataire, idFichier) -> Autorisation | None:
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
        """
    all_auto = get_all_autorizations()
    for auto in all_auto:
        if auto.idTroqueur == idTroqueur and auto.idDestinataire == idDestinataire and auto.idFichier == idFichier:
            return auto
    return None







def get_autorization_with_idFichier(idFichier):
    autorizations = []
    path = "data/demandeautorizationrecu/"
    for file in os.listdir(path):
        if file.endswith(".json"):
            try:
                data = open(path + file, encoding="utf-8")
                json_data = json.load(data)
                if json_data["idFichier"] == idFichier:
                    return Autorisation.from_json(json_data), file
            except Exception as e:
                print(f"erreur dans le fichier {e}")




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