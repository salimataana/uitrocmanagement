import json
from typing import List
from models.message import Message
import hashlib
class Troc:
    def __init__(self, id_troqueur: str,
                                 id_destinataire: str,
                                 id_fichier: str,
                                 date_fichier: str,
                                 messages: List[Message],
                                 checksum: str=None):
        self.id_troqueur = id_troqueur
        self.id_destinataire = id_destinataire
        self.id_fichier = id_fichier
        self.date_fichier = date_fichier
        self.messages = messages
        self.checksum =  hashlib.md5(f"{id_fichier}, {id_destinataire},{date_fichier},{messages}".encode('utf-8')).hexdigest() if checksum is None else checksum

    def __repr__(self):
        return (f"Troc(id_troqueur={self.id_troqueur}, id_destinataire={self.id_destinataire}, "
                f"id_fichier={self.id_fichier}, date_fichier={self.date_fichier}, "
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
            "id_troqueur": self.id_troqueur,
            "id_destinataire": self.id_destinataire,
            "id_fichier": self.id_fichier,
            "date_fichier": self.date_fichier,
            "messages": [message.to_json() for message in self.messages],
            "checksum": self.checksum
        }

    def save(self):
        with open(self.id_fichier, 'w') as fp:
            json.dump(self.to_json(), fp)

