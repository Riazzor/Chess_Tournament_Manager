from models import Player, Round, Tournament


class TournamentSerializer:
    def __init__(self) -> None:
        self.player_serializer = PlayerSerializer()
        self.round_serializer = RoundSerializer()

    def serialize(self, tournament: Tournament) -> dict:
        player_list = []
        if players := tournament.players:
            for player in players:
                player_list.append(
                    self.player_serializer.serialize(player)
                )

        round_list = []
        if rounds := tournament.rounds:
            for round_ in rounds:
                round_list.append(
                    self.round_serializer(round_)
                )

        tournament_dict = {
            'name': tournament.name,
            'place': tournament.place,
            'date': tournament.date,
            'description': tournament.description,
            'nbr_round': tournament.nbr_round,
            'rounds': round_list,
            'players': player_list,
        }
        return tournament_dict

    def deserialize(self, tournament_dict: dict) -> Tournament:
        round_list = []
        player_list = []

        rounds = tournament_dict.pop('rounds')
        players = tournament_dict.pop('players')

        if rounds:
            for round_dict in rounds:
                round_list.append(
                    self.round_serializer.deserialize(round_dict)
                )

        if players:
            for player_dict in players:
                player_list.append(
                    self.player_serializer.deserialize(player_dict)
                )
        tournament_dict['rounds'] = round_list
        tournament_dict['players'] = player_list

        return Tournament(**tournament_dict)


class PlayerSerializer:
    def serialize(self, player: Player) -> dict:
        player_dict = {
            'name': player.name,
            'surname': player.surname,
            'birthdate': player.birthdate,
            'gender': player.gender,
            'rank': player.rank,
            'score': player.score,
        }
        return player_dict

    def deserialize(self, player_dict: dict) -> Player:
        return Player(**player_dict)


class RoundSerializer:
    def serialize(self, round_: Round) -> dict:
        round_dict = {
            'name': round_.name,
            'matchs': round_.matchs,
            'start_round_time': round_.start_round_time,
            'end_round_time': round_.end_round_time,
        }

        return round_dict

    def deserialize(self, round_dict: dict) -> Round:
        return Round(**round_dict)
