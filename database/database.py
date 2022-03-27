from typing import List
from tinydb import TinyDB, where
from database.serializer import PlayerSerializer, RoundSerializer, TournamentSerializer

from models import Match, Player, Round, Tournament

databases = {
    'tournament_database': TinyDB(
        'database/tournaments.json',
        indent=4,
        separators=(',', ': '),
    ),
    'player_database': TinyDB(
        'database/players.json',
        indent=4,
        separators=(',', ': '),
    ),
}


class PlayerDB:
    def __init__(self, database: TinyDB, serializer: PlayerSerializer) -> None:
        self.player_table = database.table('players')
        self.serializer = serializer

    def create_player(self, player: Player) -> None:
        player_dict = self.serializer.serialize(player)
        self.player_table.insert(player_dict)

    def read_player(self, player_id: str) -> Player:
        players = self.player_table.search(
            where('player_id') == player_id
        )

        if not players:
            raise IndexError(
                f'The player with id {player_id} doesn\'t seem to exist'
            )
        player_dict = players[0]

        # For some f*cking unknow reason, tinydb sometimes returns an instance without the id
        # (but it returned the player so the id is clearly in the database !!)
        # and the program crash
        if 'player_id' not in player_dict:
            player_dict['player_id'] = player_id
        player = self.serializer.deserialize(player_dict)
        return player

    def list_players(self) -> List[Player]:
        table_list = self.player_table.all()
        player_list = []
        for player in table_list:
            player_list.append(
                self.serializer.deserialize(player)
            )
        return player_list

    def update_player(self, player_field: dict, player_id: str) -> Player:
        self.player_table.update(
            player_field,
            where('player_id') == player_id,
        )
        player = self.read_player(player_id)
        return player

    def delete_player(self, player_id: str) -> bool:
        removed_id = self.player_table.remove(
            where('player_id') == player_id,
        )
        if removed_id:
            return True

        return False


class TournamentDB:
    def __init__(
        self, databases: dict[str, TinyDB],
        tournament_serializer: TournamentSerializer,
        player_database,
    ) -> None:
        tournament_database = databases['tournament_database']

        self.tournament_table = tournament_database.table('tournaments')
        self.player_database = player_database
        self.tournament_serializer = tournament_serializer
        self.player_serializer = PlayerSerializer()
        self.round_serializer = RoundSerializer()

    def create_tournament(self, tournament: Tournament) -> None:
        tournament_dict = self.tournament_serializer.serialize(tournament)
        self.tournament_table.insert(tournament_dict)

    def read_tournament(self, tournament_id: str) -> Tournament:
        tournaments = self.tournament_table.search(
            where('id') == tournament_id
        )

        if not tournaments:
            raise IndexError(
                f'The tournament with id {tournament_id} doesn\'t seem to exist'
            )
        tournament_dict = tournaments[0]
        list_player_id = tournament_dict['players_id']
        player_list = self.retrieve_tournament_players(list_player_id)

        tournament = self.tournament_serializer.deserialize(
            tournament_dict, player_list)
        return tournament

    def list_tournaments(self) -> List[Tournament]:
        table_list = self.tournament_table.all()
        tournament_list = []
        for tournament_dict in table_list:
            players_id = tournament_dict['players_id']
            player_list = self.retrieve_tournament_players(players_id)

            tournament_list.append(
                self.tournament_serializer.deserialize(
                    tournament_dict, player_list)
            )
        return tournament_list

    def update_tournament(self, tournament_field: dict, tournament_id: str) -> Tournament:
        rounds = tournament_field.pop('rounds', False)
        players = tournament_field.pop('players', False)
        if rounds:
            tournament_field['rounds'] = [
                self.round_serializer.serialize(round_) for round_ in rounds
            ]
        if players:
            tournament_field['players'] = [
                self.player_serializer.serialize(player) for player in players
            ]
        self.tournament_table.update(
            tournament_field,
            where('id') == tournament_id,
        )
        tournament = self.read_tournament(tournament_id)
        return tournament

    def delete_tournament(self, tournament_id: str) -> bool:
        removed_id = self.tournament_table.remove(
            where('id') == tournament_id,
        )
        if removed_id:
            return True

        return False

    def retrieve_tournament_players(self, players_id: list) -> List[Player]:
        player_list = []
        for player_id in players_id:
            player = self.player_database.read_player(player_id)

            player_list.append(player)

        return player_list


if __name__ == '__main__':
    # from tinydb.storages import MemoryStorage
    from random import choice
    # databases.drop_tables()
    player_database = databases['player_database']
    tournament_database = databases['tournament_database']
    tournament_database.drop_tables()
    player_database.drop_tables()
    # database = TinyDB(
    #     storage=MemoryStorage
    # )
    player_serializer = PlayerSerializer()
    tournament_serializer = TournamentSerializer()
    # TOURNAMENT

    players = [
        Player('Pointud', 'Patrick', 'birthdate', 'gender', 4),
        Player('Sanika', 'Florent', 'birthdate', 'gender', 1),
        Player('Pointud', 'Émilie', 'birthdate', 'gender', 2),
        Player('Sanika', 'Nathan', 'birthdate', 'gender', 3),
        Player('Boyer', 'Marie-Huguette', 'birthdate', 'gender', 6),
        Player('Pointud', 'Magdeline', 'birthdate', 'gender', 5),
        Player('Sanika', 'Marina', 'birthdate', 'gender', 7),
        Player('Sanika', 'Johvani', 'birthdate', 'gender', 8),
        Player('Sanika', 'Mathéo', 'birthdate', 'gender', 9),
        Player('Sanika', 'Thomas', 'birthdate', 'gender', 10),
        Player('Sanika', 'Anthony', 'birthdate', 'gender', 11),
        Player('Sanika', 'Olivier', 'birthdate', 'gender', 12),
    ]
    description = '''
    This is a long long long long
    long long long long long long
    long long long long long long
    description.
    ''',
    tournaments = [
        Tournament(
            name='Paris Game',
            place='Paris 11',
            date='10/11/2022',
            description=description,
        ),
        Tournament(
            name='London Game',
            place='London street',
            date='11/10/2022',
            description=description,
        ),
        Tournament(
            name='New York Game',
            place='New York Ave',
            date='03/08/2023',
            description=description,
        ),
        Tournament(
            name='Los Angeles Game',
            place='Los Angeles 11',
            date='01/05/2022',
            description=description,
        ),
    ]
    players_duplicate = list(players)
    player_list = []
    for _ in range(8):
        player_list.append(
            players_duplicate.pop(
                choice(range(
                    len(players_duplicate)
                ))
            )
        )
    for tournament in tournaments:
        [tournament.add_player(player) for player in player_list]
    # tournament2 = Tournament(
    #     name='London Game',
    #     place='London district',
    #     date='26/04/2025',
    #     description='''
    #     This is a long long long long
    #     long long long long long long
    #     long long long long long long
    #     description.
    #     ''',
    # )
    # tournament_field = {
    #     'place': 'London',
    #     'date': '20/04/2022',
    # }
    player_db = PlayerDB(player_database, player_serializer)
    tournament_db = TournamentDB(databases, tournament_serializer, player_db)

    # tournaments = tournament_db.list_tournaments()
    matchs = [
        Match(player1, player2) for player1, player2 in zip(
            players[:len(players) // 2], players[len(players) // 2:]
        )
    ]
    for tournament in tournaments:
        tournament_db.create_tournament(tournament)
    for player in players:
        player_db.create_player(player)
    # rounds = [
    #     Round('round1', matchs)
    # ]
    for tournament in tournaments:
        tournament_rounds = [
            Round(f'Round{x}', matchs) for x in '1234'
        ]
        tournament_db.update_tournament(
            {'rounds': tournament_rounds},
            tournament.id,
        )

    # tournament_db.create_tournament(tournament1)
    # tournament_db.create_tournament(tournament2)
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
    # from pprint import pprint
    # pprint(tournament_db.list_tournaments())
    # PLAYER

    # player_db = Player_DB(database, player_serializer)
    # for player in players:
    #     player_db.create_player(player)
    # for player in players:
    #     print(player_db.read_player(player.name))

    # pprint(player_db.list_players())
