from typing import List
from models import Match, Player, Round, Tournament


class TournamentSerializer:
    def __init__(self) -> None:
        self.player_serializer = PlayerSerializer()
        self.round_serializer = RoundSerializer()

    def serialize(self, tournament: Tournament) -> dict:
        player_id_list = []
        if tournament.players:
            for player in tournament.players:
                player_id_list.append(
                    player.id
                )

        round_list = []
        if tournament.rounds:
            for round_ in tournament.rounds:
                round_list.append(
                    self.round_serializer(round_)
                )

        tournament_dict = {
            'id': tournament.id,
            'name': tournament.name,
            'place': tournament.place,
            'date': tournament.date,
            'description': tournament.description,
            'nbr_round': tournament.nbr_round,
            'rounds': round_list,
            'players_id': player_id_list,
        }
        return tournament_dict

    def deserialize(self, tournament_dict: dict, player_list: List[Player]) -> Tournament:
        rounds = tournament_dict.pop('rounds')
        _ = tournament_dict.pop('players_id')
        tournament = Tournament(**tournament_dict)
        for player in player_list:
            tournament.add_player(player)

        if rounds:
            for round_dict in rounds:
                tournament.add_round(
                    self.round_serializer.deserialize(round_dict, player_list)
                )

        return tournament


class PlayerSerializer:
    def serialize(self, player: Player) -> dict:
        player_dict = {
            'id': player.id,
            'name': player.name,
            'surname': player.surname,
            'birthdate': player.birthdate,
            'gender': player.gender,
            'rank': player.rank,
            'score': player.score,
            'opponents': player.opponents,
        }
        return player_dict

    def deserialize(self, player_dict: dict) -> Player:
        player = Player(**player_dict)
        return player


class RoundSerializer:

    def serialize(self, round_: Round) -> dict:
        match_list = []
        matchs = round_.matchs
        for match in matchs:
            match_list.append(
                {
                    'player1_id': match.player1.id,
                    'player2_id': match.player2.id,
                }
            )

        round_dict = {
            'name': round_.name,
            'matchs': match_list,
            'start_round_time': round_.start_round_time,
            'end_round_time': round_.end_round_time,
        }

        return round_dict

    def deserialize(self, round_dict: dict, player_list: List[Player]) -> Round:
        match_list = []
        matchs = round_dict.pop('matchs')
        # To reduce the number of loop we will delete players already assigned to a match.
        # To keep the original player_list intact, we assign a new one as the player_list
        # will be reused for all the rounds.
        player_list = list(player_list)
        if matchs:
            for match_dict in matchs:
                for player in list(player_list):
                    if player.id == match_dict['player1_id']:
                        player1 = player
                        player_list.remove(player)
                    elif player.id == match_dict['player2_id']:
                        player2 = player
                        player_list.remove(player)
                match_list.append(
                    Match(player1, player2)
                )

        round_dict['matchs'] = match_list

        return Round(**round_dict)
