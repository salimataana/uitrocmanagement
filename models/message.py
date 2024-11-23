import re
from typing import List
from models.objetechanger import ObjetExchange


class Message:
    def __init__(self, idMessage: str, dateMessage: str, statut: str, listeObjet: List[ObjetExchange]):
        self.idMessage = idMessage
        self.dateMessage = dateMessage
        self.statut = statut
        self.listeObjet = listeObjet


    def __repr__(self):
        return f"Message(idMessage={self.idMessage},dateMessage={self.dateMessage}, statut={self.statut}, objets={self.listeObjet})"

    def __str__(self):
        return f"Message(dateMessage={self.dateMessage}, statut={self.statut}, objets={self.listeObjet})"

    def to_json(self):
        """
        :return: this function return the object message in json format
        """
        data = {
            "idMessage": self.idMessage,
            "dateMessage": self.dateMessage,
            "statut": self.statut,
            "listeObjet": [objet.to_json() for objet in self.listeObjet]
        }
        return data