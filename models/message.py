import re
from typing import List
from models.objetechanger import ObjetExchange


class Message:
    def __init__(self, date_message: str, statut: str, objets: List[ObjetExchange]):
        self.date_message = date_message
        self.statut = statut
        self.objets = objets

    def __repr__(self):
        return f"Message(date_message={self.date_message}, statut={self.statut}, objets={self.objets})"

    def __str__(self):
        return f"Message(date_message={self.date_message}, statut={self.statut}, objets={self.objets})"

    def to_json(self):
        """
        :return: this function return the object message in json format
        """
        data = {
            "date_message": self.date_message,
            "statut": self.statut,
            "objets": [objet.to_json() for objet in self.objets]
        }
        return data