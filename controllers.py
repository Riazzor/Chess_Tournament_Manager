from typing import List
from models import Match, Player, Round, Tournament
from views import View


class Controller:
    def __init__(self, view) -> None:
        self.view: View = view

    def run(self) -> None:
        self.initiate_tournament()

        for i in range(self.tournament.nbr_round):
            # Round
            self.sort_players()
            self.create_round()

            if self.view.start_matchs(round_nbr=i+1):
                self.play_matchs()

            for match in self.round.matchs:
                self.enter_score(match)

        return None

    def initiate_tournament(self) -> None:
        # Create tournament and players:
        self.create_tournament()
        # Player
        for _ in range(8):
            player = self.create_player()
            self.tournament.add_player(player)
        print(self.tournament)

        return None

    def play_matchs(self) -> None:
        self.round.start_round()

        self.view.end_matchs()

        self.round.end_round()

        return None

    def enter_score(self, match: Match) -> None:
        player1, player2 = match.player1, match.player2
        winner = self.view.enter_match_winner(
            f'{player1.name} {player1.surname}',
            f'{player2.name} {player2.surname}',
        )
        if winner == '1':
            # Player 1 is the winner
            scores = (1, 0)
        elif winner == '2':
            scores = (0, 1)
        else:
            # Draw
            scores = (0.5, 0.5)

        match.update_score(*scores)
        return None

    def sort_players(self) -> None:
        """
        At the beginning of each round, we sort the players
        according to their score.
        If two players have the same score,
        we use their rank.
        """
        players_list = sorted(
            self.tournament.players,
            key=(lambda player: (player.score, player.rank))
        )
        self.tournament.players = players_list

        return None

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

    def create_round(self) -> None:
        round_info = self.view.get_round_info()

        # Match
        match_list = self.create_matchs()

        self.round = Round(
            round_info['name'],
            match_list
        )

        return None

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
        # since it's not supposed to happen, I'm importing choice here so it
        # happens only on rare occasion instead of each application launch.
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
    # controller.run()
    players = [
        Player(
            'the',
            'player1',
            'birthdate',
            'gender',
            1,
        ),
        Player(
            'the',
            'player2',
            'birthdate',
            'gender',
            2,
        ),
        Player(
            'the',
            'player3',
            'birthdate',
            'gender',
            3,
        ),
        Player(
            'the',
            'player4',
            'birthdate',
            'gender',
            4,
        ),
        Player(
            'the',
            'player5',
            'birthdate',
            'gender',
            5,
        ),
        Player(
            'the',
            'player6',
            'birthdate',
            'gender',
            6,
        ),
        Player(
            'the',
            'player7',
            'birthdate',
            'gender',
            7,
        ),
        Player(
            'the',
            'player8',
            'birthdate',
            'gender',
            8,
        ),
    ]

    controller.tournament = Tournament(
        'Tournament',
        'place',
        'date',
        'description',
    )

    for player in players:
        controller.tournament.add_player(player)

    for i in range(controller.tournament.nbr_round):
        print(f'Tour {i+1} : ')
        controller.sort_players()
        controller.create_round()
        controller.play_matchs()
        for match in controller.round.matchs:
            controller.enter_score(match)
        print(controller.round)

    # tournament = controller.create_tournament()
    # print(tournament)

    # player = controller.create_player()
    # print(player.__dict__)
