from datetime import datetime
from typing import List
import uuid


class Player:
    players_instance = []

    def __init__(
        self, name: str, surname: str,
        birthdate: str, gender: str,
        rank: int, score: float = 0, id: str = None,
        opponents: list = None
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.gender = gender
        self.score = score
        self.rank = rank
        self.opponents = opponents or []

        self.update_rank(rank)

    def __repr__(self) -> str:
        return f'Player : {self.name} {self.surname} {self.rank}'

    def update_rank(self, rank: int) -> None:
        # First we remove if already existent instance
        for index, id in enumerate([player.id for player in self.players_instance]):
            if self.id == id:
                self.players_instance.pop(index)
                break

        # Insert at new rank
        self.players_instance.insert(rank - 1, self)

        # update every player's rank
        for index, player in enumerate(self.players_instance, 1):
            player.rank = index


class Match:
    """
    A match contains the instances of the
    two players.

    It contains one method to update the players scores.

    The init takes just the player and the score is entered
    by the referee at the end of the game.
    """

    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2

    def update_score(self, score1, score2) -> None:
        self.player1.score += score1
        self.player2.score += score2

    def __repr__(self) -> str:
        return (
            f'<Match> instance : {self.player1.name} {self.player1.surname}' +
            '  -vs-  ' +
            f'{self.player2.name} {self.player2.surname}'
        )

    def __str__(self) -> str:
        return (
            f'Match : \n{self.player1.name} {self.player1.surname}' +
            '  -vs-  ' +
            f'{self.player2.name} {self.player2.surname}'
        )


class Round:
    def __init__(self, name: str, matchs: List[Match], start_round_time: str = "", end_round_time: str = "") -> None:
        self.name = name
        self.matchs = matchs
        self.start_round_time = start_round_time
        self.end_round_time = end_round_time

    def start_round(self) -> None:
        self.start_round_time = datetime.now().strftime('%d/%m/%Y - %H:%M')

    def end_round(self) -> None:
        self.end_round_time = datetime.now().strftime('%d/%m/%Y - %H:%M')

    def __repr__(self) -> str:
        representation = 'Round : \n'
        if self.matchs:
            for match in self.matchs:
                representation += str(match) + '\n'
            if self.end_round_time:
                representation += '{}  __  {}'.format(
                    self.start_round_time,
                    self.end_round_time
                )
        else:
            representation += 'no matchs yet.'

        return representation


class Tournament:
    def __init__(
        self, name: str, place: str, date: str,
        description: str, nbr_round: int = 4, time_control: str = None,
        id: str = None, rounds: List[Round] = None, players: List[Player] = None,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.place = place
        self.date = date
        self.description = description
        self.nbr_round = nbr_round
        self.rounds = rounds or []
        self.players = players or []
        self.time_control = time_control

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round_: Round):
        self.rounds.append(round_)

    def __repr__(self) -> str:
        return f'Tournament : {self.name} \n{self.description}'
