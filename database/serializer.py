from models import Player, Tournament


class TournamentSerializer:
    def serialize(self, tournament: Tournament) -> dict:
        player_list = []
        if players := tournament.players:
            player_serializer = PlayerSerializer()
            for player in players:
                player_list.append(
                    player_serializer.serialize(player)
                )

        tournament_dict = {
            'name': tournament.name,
            'place': tournament.place,
            'date': tournament.date,
            'description': tournament.description,
            'nbr_round': tournament.nbr_round,
            # When we have player serializer, we serialize them all before hand.
            'players': player_list,
        }
        return tournament_dict

    def deserialize(self, tournament_dict: dict) -> Tournament:
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
