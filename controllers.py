
from typing import List
from models import Match, Player, Tournament
from views import View


class Controller:
    def __init__(self, view) -> None:
        self.view = view

    def run(self) -> None:
        self.create_tournament()
        # Player
        for _ in range(2):
            player = self.create_player()
            self.tournament.add_player(player)
        print(self.tournament)

        # Match
        self.sort_for_match()
        match_list = self.create_matchs()
        print(match_list)

        return None

    def sort_for_match(self) -> None:
        """
        At the end of each round, we sort the players
        according to their score.
        If two players have the same score,
        we use their rank.
        """
        players_list = sorted(
            self.tournament.players,
            key=(lambda player: (player.score, player.rank))
        )
        self.tournament.players = players_list

    def create_tournament(self) -> None:
        tournament_info = self.view.get_tournament_info()
        tournament = Tournament(
            tournament_info['name'],
            tournament_info['place'],
            tournament_info['date'],
            tournament_info['description'],
        )
        self.tournament = tournament

        return None

    def create_player(self) -> Player:
        player_info = self.view.get_player_info()
        player = Player(
            player_info['name'],
            player_info['surname'],
            player_info['birthdate'],
            player_info['gender'],
            int(player_info['rank']),
            int(player_info['score'])
        )

        return player

    def create_matchs(self) -> List[Match]:
        """
        The swiss system is used :
        The list of player (after being sorted) is split in
        two sublist (S1 and S2).
        The first of S1 plays against the first of S2,
        the second of S1 against the second of S2, and
        so on so that the last player of S1
        plays against the last player of S2.
        """
        players_list = self.tournament.players
        middle = len(players_list) // 2
        is_not_even = len(players_list) % 2
        firs_half, second_half = players_list[:middle], players_list[middle:]
        match_list = [
            (player1, player2)
            for player1, player2 in zip(firs_half, second_half)
        ]
        matchs = list()
        for match in match_list:
            player1, player2 = match
            matchs.append(
                Match(player1, player2)
            )

        # should not happen but this part handles an odd number of players :
        if is_not_even:
            from random import choice
            # a random player will be choosed to play a second time.
            matchs.append(
                Match(
                    players_list[-1],           # player1
                    choice(players_list[:-1])   # player2
                )
            )
            del choice

        return matchs


if __name__ == '__main__':
    view = View()
    controller = Controller(view)
    controller.run()
    # tournament = controller.create_tournament()
    # print(tournament)

    # player = controller.create_player()
    # print(player.__dict__)
