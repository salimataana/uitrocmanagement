

class ObjetExchange:
    def __init__(self, titre: str, description: str, qualite: int, quantite: int):
        self.titre = titre
        self.description = description
        self.qualite = qualite
        self.quantite = quantite

    def __repr__(self):
        return f"Objet(titre={self.titre}, description={self.description}, qualite={self.qualite}, quantite={self.quantite})"


