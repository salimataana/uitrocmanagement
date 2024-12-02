import json
import os

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

def apply_control(file_name):
    # Vérification de la taille du fichier
    file_stats = os.stat(file_name)
    size_file_kb = file_stats.st_size / 1024
    if size_file_kb > 2:
        print(f"{file_name} est rejeté car sa taille est de {size_file_kb:.2f} Ko > 2 Ko")
        return

    # Ouverture et chargement du fichier JSON
    with open(file_name, encoding="utf-8") as file:
        json_data = file.read()

    # Vérification du nombre de caractères
    if len(json_data) > 1000:
        print(f"{file_name} est rejeté car il contient plus de 1000 caractères")
        return

    # Validation du schéma JSON
    validate_json(file_path=file_name, validation_schema="")
    print("Schéma validé")

    troc = Troc.from_json(json.loads(json_data))
    nbr_message = len(troc.messages)

    # Vérification du nombre de messages
    if nbr_message != troc.nombre_messages:
        print("Fichier non valide : nombre de messages différent")
