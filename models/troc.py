import json
from typing import List


from models.message import Message
import hashlib
class Troc:
    def __init__(self, idTroqueur: str,
                                 idDestinataire: str,
                                 idFichier: str,
                                 dateFichier: str,

                                 messages: List[Message],
                                 checksum: str=None):
        self.idTroqueur = idTroqueur
        self.idDestinataire = "" if idDestinataire is None else idDestinataire
        self.idFichier = idFichier
        self.dateFichier = dateFichier
        self.messages = messages
        self.checksum =  hashlib.md5(f"{idFichier}, {idDestinataire},{dateFichier},{messages}".encode('utf-8')).hexdigest() if checksum is None else checksum

    def __repr__(self):
        return (f"Troc(idTroqueur={self.idTroqueur}, idDestinataire={self.idDestinataire}, "
                f"idFichier={self.idFichier}, dateFichier={self.dateFichier}"
                f"messages={self.messages}, checksum={self.checksum})")

    @staticmethod
    def from_json(data_json):
        """
        :param data_json: input data to initialize the object troc
        :return: this function return an object of troc from json pass in input
        """
        return Troc(**data_json)

    def to_json(self):
        """
        :return: this function return the object troc in json format
        """
        return {
            "idTroqueur": self.idTroqueur,
            "idDestinataire": self.idDestinataire,
            "idFichier": self.idFichier,
            "dateFichier": self.dateFichier,
            "messages": [message.to_json() if not isinstance(message,dict) else message for message in self.messages],
            "checksum": self.checksum
        }

    def save(self, path):
        with open(path, 'w') as fp:
            json.dump(self.to_json(), fp)

