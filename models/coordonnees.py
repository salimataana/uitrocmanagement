class Coordonnees:
    def __init__(self, mail: str, telephone: str, nomAuteur: str):
        self.mail = mail
        self.telephone = telephone
        self.nomAuteur = nomAuteur

    def __repr__(self):
            return f"Coordonnees(mail={self.mail}, telephone={self.telephone}, nomAuteur={self.nomAuteur})"

    def to_json(self):
        """
        :return: this function return the object coords in json format
        """
        data = {
            "mail": self.mail,
            "telephone": self.telephone,
            "nomAuteur": self.nomAuteur,
        }
        return data