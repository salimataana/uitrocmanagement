import json
import os
from jsonschema import validate
from models.troc import Troc
DATA_FOLDER="data"

def validate_json(file_path, validation_schema):
    try:
        file = open(file_path, 'r')
        data = json.load(file)
        file = open(validation_schema, 'r')
        schema = json.load(file)
        return validate(instance=data, schema=schema)
    except json.JSONDecodeError:
        print("Le json n'est pas valide")
        return False

def get_all_trocs(folder_path):
    noms_fichers_pas_bons=[]
    trocs=[]
    for file in os.listdir(folder_path):
        # check the files which are end with specific extension
        if file.endswith(".json"):
            # print path name of selected files
            try:
                #retenir quelque part le nom du fichier
                trocs.append(get_troc(os.path.join(folder_path, file)))
                trocs.append(
                                        {
                                            "file_name":file,
                                            "troc":get_troc(os.path.join(folder_path, file))
                                        }
                )
            except Exception as e:
                noms_fichers_pas_bons.append(file),
                print(f"erreur dans le fichier {e}")
    return trocs,noms_fichers_pas_bons


def get_troc(path):
    """
    :param path: on verifie d'abord si le fichier est un bon json avant de le charger dans troc
    :return:
    """
    is_valid = validate_json(path, "schema/schema.json")
    file = open(path,encoding="utf-8")
    json_data = json.load(file)
    troc = Troc.from_json(json_data)
    return troc

"""print(get_all_trocs())"""