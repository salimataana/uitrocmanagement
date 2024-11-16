import re
from typing import List

from models.message import Message

class Troc:
    def __init__(self, id_troqueur: str, id_destinataire: str, id_fichier: str, date_fichier: str,
                 messages: List[Message], checksum: str):
        self.id_troqueur = id_troqueur
        self.id_destinataire = id_destinataire
        self.id_fichier = id_fichier
        self.date_fichier = date_fichier
        self.messages = messages
        self.checksum = checksum

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
