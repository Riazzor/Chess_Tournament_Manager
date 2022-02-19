from typing import List
from tinydb import TinyDB, where
from database.serializer import PlayerSerializer, TournamentSerializer

from models import Player, Tournament

database = TinyDB(
    'database/Chess_tournament.json',
    indent=4,
    separators=(',', ': '),
)


class Tournament_DB:
    def __init__(self, database: TinyDB, serializer: TournamentSerializer) -> None:
        self.tournament_table = database.table('tournaments')
        self.serializer = serializer

    def create_tournament(self, tournament: Tournament) -> None:
        tournament_dict = self.serializer.serialize(tournament)
        self.tournament_table.insert(tournament_dict)

    def read_tournament(self, tournament_name: str) -> Tournament:
        tournament = self.tournament_table.search(
            where('name') == tournament_name
        )[0]
        tournament = self.serializer.deserialize(tournament)
        return tournament

    def list_tournaments(self) -> List[Tournament]:
        table_list = self.tournament_table.all()
        tournament_list = []
        for tournament in table_list:
            tournament_list.append(
                self.serializer.deserialize(tournament)
            )
        return tournament_list

    def update_tournament(self, tournament_field: dict, tournament_name: str) -> Tournament:
        self.tournament_table.update(
            tournament_field,
            where('name') == tournament_name,
        )
        tournament = self.read_tournament(tournament_name)
        tournament = self.serializer.deserialize(tournament)
        return tournament

    def delete_tournament(self, tournament_name: str) -> bool:
        removed_id = self.tournament_table.remove(
            where('name') == tournament_name,
        )
        if removed_id:
            return True

        return False


class Player_DB:
    def __init__(self, database: TinyDB, serializer: PlayerSerializer) -> None:
        self.player_table = database.table('players')
        self.serializer = serializer

    def create_player(self, player: Player) -> None:
        player_dict = self.serializer.serialize(player)
        self.player_table.insert(player_dict)

    def read_player(self, player_name: str) -> Player:
        player = self.player_table.search(
            where('name') == player_name
        )[0]
        player = self.serializer.deserialize(player)
        return player

    def list_players(self) -> List[Player]:
        table_list = self.player_table.all()
        player_list = []
        for player in table_list:
            player_list.append(
                self.serializer.deserialize(player)
            )
        return player_list

    def update_player(self, player_field: dict, player_name: str) -> Player:
        self.player_table.update(
            player_field,
            where('name') == player_name,
        )
        player = self.read_player(player_name)
        player = self.serializer.deserialize(player)
        return player

    def delete_player(self, player_name: str) -> bool:
        removed_id = self.player_table.remove(
            where('name') == player_name,
        )
        if removed_id:
            return True

        return False


if __name__ == '__main__':
    from tinydb.storages import MemoryStorage
    database.drop_tables()
    database = TinyDB(
        storage=MemoryStorage
    )
    player_serializer = PlayerSerializer()
    tournament_serializer = TournamentSerializer()
    # TOURNAMENT

    players = [
        Player(
            'Pointud',
            'Patrick',
            'birthdate',
            'gender',
            4,
        ),
        Player(
            'Sanika',
            'Florent',
            'birthdate',
            'gender',
            1,
        ),
        Player(
            'Pointud',
            'Émilie',
            'birthdate',
            'gender',
            2,
        ),
        Player(
            'Sanika',
            'Nathan',
            'birthdate',
            'gender',
            3,
        ),
        Player(
            'Boyer',
            'Marie-Huguette',
            'birthdate',
            'gender',
            6,
        ),
        Player(
            'Pointud',
            'Magdeline',
            'birthdate',
            'gender',
            5,
        ),
        Player(
            'Sanika',
            'Johvani',
            'birthdate',
            'gender',
            8,
        ),
        Player(
            'Sanika',
            'Marina',
            'birthdate',
            'gender',
            7,
        ),
    ]
    tournament1 = Tournament(
        name='Paris Game',
        place='Paris 11',
        date='11/10/2022',
        description='''
        This is a long long long long
        long long long long long long
        long long long long long long
        description.
        ''',
    )
    for player in players:
        tournament1.add_player(player)
    tournament2 = Tournament(
        name='London Game',
        place='London district',
        date='26/04/2025',
        description='''
        This is a long long long long
        long long long long long long
        long long long long long long
        description.
        ''',
    )
    # tournament_field = {
    #     'place': 'London',
    #     'date': '20/04/2022',
    # }
    tournament_db = Tournament_DB(database, tournament_serializer)
    tournament_db.create_tournament(tournament1)
    tournament_db.create_tournament(tournament2)
    # print(tournament_db.read_tournament(tournament2['name']))
    # fetch_tournament = tournament_db.read_tournament('Paris Game')
    # tournament_list = tournament_db.list_tournaments()
    # tournament_db.update_tournament(
    #     tournament_field,
    #     tournament2['name'],
    # )
    # good_tournament = {
    #     'name': 'London Game',
    # }
    # bad_tournament = {
    #     'name': 'Londoni Game',
    # }
    # assert tournament_db.delete_tournament(bad_tournament['name']) is False
    # assert tournament_db.delete_tournament(good_tournament['name']) is True
    # assert tournament_db.delete_tournament(good_tournament['name']) is False
    # print(tournament_db.read_tournament('London Game'))
    from pprint import pprint
    pprint(tournament_db.list_tournaments())
    # PLAYER

    player_db = Player_DB(database, player_serializer)
    for player in players:
        player_db.create_player(player)
    # for player in players:
    #     print(player_db.read_player(player.name))

    pprint(player_db.list_players())
