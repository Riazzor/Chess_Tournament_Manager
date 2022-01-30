
class Tournament:
    def __init__(self, name, place, date, description) -> None:
        self.name = name
        self.place = place
        self.date = date
        self.description = description
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def __repr__(self) -> str:
        return f'Tournament : {self.name} {self.description}'


class Player:
    def __init__(self, name, surname, birthdate, gender, rank, score=0) -> None:
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.score = score

    def __repr__(self) -> str:
        return f'Player : {self.name} {self.surname}'


class Match:
    """
    A match contains two lists.
    Each list contains two elements :
        - one reference to the player
        - the player's score at the end of the match.

    The init takes just the player and the score is entered
    by the referee at the end of the game.
    """

    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = [player1]
        self.player2 = [player2]

    def set_score(self, score1, score2):
        self.player1.append(score1)
        self.player2.append(score2)

    def __repr__(self) -> str:
        return f'Match : {self.player1[0].name}  -vs-  {self.player2[0].name}'

    def __str__(self) -> str:
        return f'Match : {self.player1[0].name}  -vs-  {self.player2[0].name}'
