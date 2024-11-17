from typing import List

from models.coordonnees import Coordonnees


class DemandeAutorisation:
    def __init__(self, statut_autorisation: str, date: str, id_message: str, coord:Coordonnees):
        self.statut_autorisation = statut_autorisation
        self.date = date
        self.id_message = id_message
        self.coord = coord

    def __repr__(self):
            return f"DemandeAutorisation(statut_autorisation={self.statut_autorisation}, date={self.date}, id_message={self.id_message}, coord={self.coord})"

    def __str__(self):
            return f"DemandeAutorisation(statut_autorisation={self.statut_autorisation}, date={self.date}, id_message={self.id_message}, coord={self.coord})"

    def to_json(self):
            """
            :return: this function return the object demandeautorisation in json format
            """
            data = {
                "statut_autorisation": self.statut_autorisation,
                "date": self.date,
                "id_message": self.id_message,
                "coord": self.coord.to_json() 
            }
            return data