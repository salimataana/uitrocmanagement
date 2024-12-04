import json
import os

from constant import GROUP_NUMBER
from data_access.validation_helper import validate_json
from models.autorisation import Autorisation
from models.troc import Troc

DATA_FOLDER_AUTORIZATION = "data/demandeautorizationrecu"

def get_autorization_by_id_fichier(id_fichier) -> Autorisation:
    """
    :param id_fichier: On vérifie d'abord si le fichier est un bon JSON avant de le charger dans Autorisation
    :return: Instance d'Autorisation
    """
    file = open(id_fichier, encoding="utf-8")
    json_data = json.load(file)
    return Autorisation.from_json(json_data)

def get_all_autorizations(folder_path=DATA_FOLDER_AUTORIZATION):
    autorizations = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            try:
                autorizations.append(get_autorization_by_id_fichier(os.path.join(folder_path, file)))
            except Exception as e:
                print(f"Erreur dans le fichier {e}")
    return autorizations

def filter_autorization_by_id_troqueur_id_destinateur_id_fichier(idTroqueur, idDestinataire, idFichier) -> Autorisation | None:
    """
    :param idTroqueur: Identifiant du troqueur
    :param idDestinataire: Identifiant du destinataire
    :param idFichier: Identifiant du fichier
    :return: Autorisation correspondante ou None
    """
    all_auto = get_all_autorizations()
    for auto in all_auto:
        if auto.idTroqueur == idTroqueur and auto.idDestinataire == idDestinataire and auto.idFichier == idFichier:
            return auto
    return None

def get_autorization_with_idFichier(idFichier):
    path = "data/demandeautorizationrecu/"
    for file in os.listdir(path):
        if file.endswith(".json"):
            try:
                with open(path + file, encoding="utf-8") as data:
                    json_data = json.load(data)
                    if json_data["idFichier"] == idFichier:
                        return Autorisation.from_json(json_data), file
            except Exception as e:
                print(f"Erreur dans le fichier {e}")


def validate_autorization_file(id_fichier):
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
        """
    # recuperation des personne autorisé ou groupe // grace au dossier demandeautorizationaccepted

    count_fails = 0
    message = ""
    file_stats = os.stat(id_fichier)
    size_file_bytes = file_stats.st_size / 1000

    print("validate_troc_file", id_fichier)
    print("La taille du fichier ", id_fichier, " est de ", size_file_bytes)

    # verifie de la taille
    if size_file_bytes > 2:
        count_fails += 1
        message = f"{id_fichier} est rejété car sa taille est de {size_file_bytes} > 2 \n"

    # verifie du schema
    try:
        is_valid = validate_json(id_fichier, "schema/schema_autorisation.json")
        file = open(id_fichier, encoding="utf-8")
        json_data = json.load(file)
    except Exception as e:
        count_fails += 1
        message = message + f"{id_fichier} est rejété car le fichier n'est pas un bon json \n"
        return (message, count_fails)

    # verification du checksum : nombre de messages

    # compter nombre de caractere
    with open(id_fichier, 'r') as file:
        text = file.read().strip().split()
        len_chars = sum(len(word) for word in text)

    if len_chars > 1000:
        count_fails += 1
        message = message + f"{id_fichier} est rejété car le nombre de caractere est superieur à 1000 \n"


    ## reste a faire : autorisation non present et fichier deja traité
    return (message, count_fails)


def check_all_file(folder):
    check = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if validate_autorization_file(file_path)[1] >0:
            check.append({"idFichier": file, "cause":validate_autorization_file(file_path)[0], "nombreCheckpasValide": validate_autorization_file(file_path)[1]  })

    return check