import json
from jsonschema import validate


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
