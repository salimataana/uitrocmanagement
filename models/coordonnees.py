class Coordonnees:
    def __init__(self, mail: str, telephone: str):
        self.mail = mail
        self.telephone = telephone

    def __repr__(self):
            return f"Coords(mail={self.mail}, telephone={self.telephone})"

    def to_json(self):
        """
        :return: this function return the object coords in json format
        """
        data = {
            "mail": self.mail,
            "telephone": self.telephone,
        }
        return data