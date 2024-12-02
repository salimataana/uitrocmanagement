from typing import List

from models.coordonnees import Coordonnees


class MessageDemandeAutorisation:
    def __init__(self,
                                date: str,
                                idMessage: str,
                                statutAutorisation: str,
                                coordonnees: Coordonnees):
        self.statutAutorisation = statutAutorisation
        self.date = date
        self.idMessage = idMessage
        self.coordonnees = coordonnees

    def __repr__(self):
            return f"MessageDemandeAutorisation(statutAutorisation={self.statutAutorisation}, date={self.date}, idMessage={self.idMessage}, coordonnees={self.coordonnees})"

    def __str__(self):
            return f"MessageDemandeAutorisation(statutAutorisation={self.statutAutorisation}, date={self.date}, idMessage={self.idMessage}, coordonnees={self.coordonnees})"

    @staticmethod
    def from_json(data_json):
        return MessageDemandeAutorisation(**data_json)


    def to_json(self):
            """
            :return: this function return the object MessageDemandeAutorisation in json format
            """
            coord =Coordonnees(**self.coordonnees) if isinstance(self.coordonnees, dict) else self.coordonnees
            data = {
                "idMessage": self.idMessage,
                "statutAutorisation": self.statutAutorisation,
                "date": self.date,
                "coordonnees": coord.to_json()
            }
            return data