

class ObjetExchange:
    def __init__(self, titre: str, description: str, qualite: int, quantite: int):
        self.titre = titre
        self.description = description
        self.qualite = qualite
        self.quantite = quantite

    def __repr__(self):
        return f"Objet(titre={self.titre}, description={self.description}, qualite={self.qualite}, quantite={self.quantite})"


    def to_json(self):
        """
        :return: this function return the object objet in json format
        """
        data = {
            "titre": self.titre,
            "description": self.description,
            "qualite": self.qualite,
            "quantite": self.quantite
        }
        return data