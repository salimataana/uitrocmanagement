import hashlib
from typing import List

from flask import json

from models.demandeautorisation import DemandeAutorisation


class Autorisation:
    def __init__(self, id_troqueur: str, id_destinataire: str, id_fichier: str, date_fichier:str, demande_autorisation: DemandeAutorisation, checksum: str=None):
        self.id_troqueur = id_troqueur
        self.id_destinataire = id_destinataire
        self.id_fichier = id_fichier
        self.date_fichier = date_fichier
        self.checksum = hashlib.md5(f"{id_fichier}, {id_destinataire},{date_fichier}".encode('utf-8')).hexdigest() if checksum is None else checksum
        self.demande_autorisation = demande_autorisation

    def __repr__(self):
        return f"Autorisation(id_troqueur={self.id_troqueur}, id_destinataire={self.id_destinataire}, id_fichier={self.id_fichier}, checksum={self.checksum}, demandes_autorisation={self.demande_autorisation})"

    @staticmethod
    def from_json(data_json):
        """
        :param data_json: input data to initialize the object autorisations
        :return: this function return an object of autorisations from json pass in input
        """
        return Autorisation(**data_json)

    def to_json(self):
        """
        :return: this function return the object autorisations in json format
        """
        return {
            "id_troqueur": self.id_troqueur,
            "id_destinataire": self.id_destinataire,
            "id_fichier": self.id_fichier,
            "date_fichier": self.date_fichier,
            "demandes_autorisation": self.demande_autorisation.to_json(),
            "checksum": self.checksum
        }

    def save(self, path):
        with open(path, 'w') as fp:
            json.dump(self.to_json(), fp)



