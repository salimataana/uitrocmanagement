import json
import os

from jsonschema.validators import extend

from constant import GROUP_NUMBER
from data_access.data_access_autorization import get_all_autorizations
from data_access.validation_helper import validate_json
from models.troc import Troc
from models.user import TrocModel
from database import db
def get_troc_by_id_fichier(folder , id_fichier) -> Troc:
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
    """

    for file_name in os.listdir(folder):
        if file_name.endswith(".json"):
            # print path name of selected files
            try:
                troc = get_troc_by_file_name(os.path.join(folder, file_name))
                if troc.idFichier==id_fichier:
                    return troc, file_name
            except Exception as e:
                    print(f"erreur dans le fichier {e}")


    return None, None


def get_troc_by_file_name(id_fichier) -> Troc:
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
    """
    print("get_troc_by_file_name",id_fichier)
    try:
        is_valid = validate_json(id_fichier, "schema/schema_troc.json")
    except Exception as e:
        print(f"erreur dans le fichier {e}")
    file = open(id_fichier, encoding="utf-8")
    json_data = json.load(file)
    return Troc.from_json(json_data)


def validate_troc_file(id_fichier):
    """
        :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
        :return:
        """
    # recuperation des personne autorisé ou groupe // grace au dossier demandeautorizationaccepted
    list_groupe_autoirise_dest = [item.idDestinataire for item in get_all_autorizations("data/demandeautorisationaccepted")]
    list_groupe_autoirise_troq = [item.idTroqueur for item in get_all_autorizations("data/demandeautorisationaccepted")]
    list_groupe_autoirise = list_groupe_autoirise_dest + list_groupe_autoirise_troq

    count_fails = 0
    message = ""
    file_stats = os.stat(id_fichier)
    size_file_bytes = file_stats.st_size / 1000

    print("validate_troc_file",id_fichier)
    print("La taille du fichier ",id_fichier, " est de ",size_file_bytes)

    # verifie de la taille
    if size_file_bytes > 2:
        count_fails += 1
        message = f"{id_fichier} est rejété car sa taille est de {size_file_bytes} > 2 \n"

    # verifie du schema
    try:
        is_valid = validate_json(id_fichier, "schema/schema_troc.json")
        file = open(id_fichier, encoding="utf-8")
        json_data = json.load(file)
    except Exception as e:
        count_fails += 1
        message = message + f"{id_fichier} est rejété car le fichier n'est pas un bon json  \n"
        return (message, count_fails)

    # verification du checksum : nombre de messages


    # compter nombre de caractere
    with open(id_fichier, 'r') as file:
        text = file.read().strip().split()
        len_chars = sum(len(word) for word in text)

    if len_chars > 1000:
        count_fails += 1
        message = message + f"{id_fichier} est rejété car le nombre de caractere est superieur à 1000 \n"

    if json_data["idTroqueur"] == GROUP_NUMBER:
        if json_data["idDestinataire"] not in list_groupe_autoirise:
            count_fails += 1
            message = message + f"{id_fichier} est rejété car le destinataire  {json_data["idDestinataire"]} n'est pas autorisé \n"
        pass
    if json_data["idDestinataire"] == GROUP_NUMBER:
        if json_data["idTroqueur"] not in list_groupe_autoirise:
            count_fails += 1
            message = message + f"{id_fichier} est rejété car le destinataire {json_data["idTroqueur"]} n'est pas autorisé \n"

    if json_data["idDestinataire"] != GROUP_NUMBER and json_data["idTroqueur"]  != GROUP_NUMBER :
            count_fails += 1
            message = message + f"{id_fichier} est rejété car le groupe ne figure dans le destinataire ni le troqueur :  {json_data["idTroqueur"]} || {json_data["idDestinataire"]} \n"

    ## reste a faire : autorisation non present et fichier deja traité
    return (message, count_fails)


def get_all_trocs_well_formatted(folder_path, well_files=[]):
    list_trocs=[]
    if len(well_files)==0:
        well_files = os.listdir(folder_path)
    else:
        well_files = [os.path.join(folder_path, item) for item in well_files]
    for file in well_files:
        # check the files which are end with specific extension
        if file.endswith(".json"):
            # print path name of selected files
            try:
                #retenir quelque part le nom du fichier
                list_trocs.append(get_troc_by_file_name(os.path.join(file)))
            except Exception as e:
                print(f"erreur dans le fichier {e}")
    return list_trocs


def get_all_trocs_malformated(folder_path):
    trocs_malformated = {}
    for file in os.listdir(folder_path):
        trocs_malformated[file] = validate_troc_file(os.path.join(folder_path, file))
    return trocs_malformated

def get_all_trocs(folder_path):
    malformatted_files =  get_all_trocs_malformated(folder_path)
    print(malformatted_files)
    well_files = []
    for key, value  in malformatted_files.items():
        if value[1] == 0:
            well_files.append(key)

    well_formated_files = get_all_trocs_well_formatted(folder_path, well_files)
    malformatted_files = [{"idFichier":key,"nombreCheckpasValide" :value[1],"cause": value[0]} for key, value  in malformatted_files.items() if value[1] > 0]
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

