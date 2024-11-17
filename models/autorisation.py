from typing import List

from flask import json

from models.demandeautorisation import DemandeAutorisation


class Autorisation:
    def __init__(self, id_troqueur: str, id_destinataire: str, id_fichier: str, date_fichier:str, checksum: str, demandes_autorisation: List[DemandeAutorisation]):
        self.id_troqueur = id_troqueur
        self.id_destinataire = id_destinataire
        self.id_fichier = id_fichier
        self.date_fichier = date_fichier
        self.checksum = None
        self.demandes_autorisation = demandes_autorisation

    def __repr__(self):
        return f"Autorisation(id_troqueur={self.id_troqueur}, id_destinataire={self.id_destinataire}, id_fichier={self.id_fichier}, checksum={self.checksum}, demandes_autorisation={self.demandes_autorisation})"

    @staticmethod
    def from_json(data_json):
        """
        :param data_json: input data to initialize the object autorisation
        :return: this function return an object of autorisation from json pass in input
        """
        return Autorisation(**data_json)

    def to_json(self):
        """
        :return: this function return the object autorisation in json format
        """
        return {
            "id_troqueur": self.id_troqueur,
            "id_destinataire": self.id_destinataire,
            "id_fichier": self.id_fichier,
            "date_fichier": self.date_fichier,
            "demandes_autorisation": [demande_autorisation.to_json() for demande_autorisation in self.demandes_autorisation],
            "checksum": self.checksum
        }

    def save(self):
        with open(self.id_fichier, 'w') as fp:
            json.dump(self.to_json(), fp)



