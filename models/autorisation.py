import hashlib
from typing import List

from flask import json

from models.demandeautorisation import MessageDemandeAutorisation


class Autorisation:
    def __init__(self, idTroqueur: str, idDestinataire: str, idFichier: str, dateFichier:str, messageDemandeAutorisation: MessageDemandeAutorisation, checksum: str=None):
        self.idTroqueur = idTroqueur
        self.idDestinataire = idDestinataire
        self.idFichier = idFichier
        self.dateFichier = dateFichier
        self.checksum = hashlib.md5(f"{idFichier}, {idDestinataire},{dateFichier}".encode('utf-8')).hexdigest() if checksum is None else checksum
        self.messageDemandeAutorisation = messageDemandeAutorisation

    def __repr__(self):
        return f"Autorisation(idTroqueur={self.idTroqueur}, idDestinataire={self.idDestinataire}, idFichier={self.idFichier}, checksum={self.checksum}, messageDemandeAutorisation={self.messageDemandeAutorisation})"

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
        message = MessageDemandeAutorisation(**self.messageDemandeAutorisation) if isinstance(self.messageDemandeAutorisation, dict) else self.messageDemandeAutorisation
        return {
            "idTroqueur": self.idTroqueur,
            "idDestinataire": self.idDestinataire,
            "idFichier": self.idFichier,
            "dateFichier": self.dateFichier,
            "messageDemandeAutorisation": message.to_json(),
            #"messageDemandeAutorisation": self.messageDemandeAutorisation,
            "checksum": self.checksum
        }

    def save(self, path):
        with open(path, 'w') as fp:
            json.dump(self.to_json(), fp)



