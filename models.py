from datetime import datetime
from typing import List
import uuid


class Player:
    def __init__(
        self, name: str, surname: str,
        birthdate: str, gender: str,
        rank: int, score: int = 0, id: str = None,
    ) -> None:
        self.id = id or str(uuid.uuid4())
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
        self.start_round_time = datetime.now().strftime('%x - %H:%M')

    def end_round(self) -> None:
        self.end_round_time = datetime.now().strftime('%x - %H:%M')

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
        description: str, nbr_round: int = 4, id: str = None,
        rounds: List[Round] = None, players: List[Player] = None,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.place = place
        self.date = date
        self.description = description
        self.nbr_round = nbr_round
        self.rounds = rounds or []
        self.players = players or []

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round_: Round):
        self.rounds.append(round_)

    def __repr__(self) -> str:
        return f'Tournament : {self.name} \n{self.description}'
