
class Tournament:
    def __init__(self, name, place, date, description) -> None:
        self.name = name
        self.place = place
        self.date = date
        self.description = description

    def add_player(self, player):
        self.player = player


class Player:
    def __init__(self, name, surname, birthdate, gender, rank, score=0) -> None:
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.score = score
