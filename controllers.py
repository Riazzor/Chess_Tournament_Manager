from typing import List, Optional
from functions import sub_menu, table_factory
from models import Match, Player, Round, Tournament
from views import ReportView, View


class ReportController:
    def __init__(self) -> None:
        self.report_view = ReportView()
        self.tournament_database = table_factory('tournaments')
        self.player_database = table_factory('players')

    @sub_menu
    def run(self) -> str:
        # some function to choose what to display.
        choice = self.report_view.main_menu()
        report_option = {
            '1': self.actors_report,
            '2': self.tournament_report,
            # how to go back to previous menu (main)
            'q': lambda: None,
        }

        report_option[choice]()

        return choice

    def actors_list(self) -> List[Player]:
        """
        Fetch all players in database.
        """
        return self.player_database.list_players()

    @sub_menu
    def actors_report(self) -> str:
        """
        Displays all known players name and surname.
        """
        players_list = self.actors_list()
        order_choice = self.report_view.report_sort_choice()
        # Alphabétique
        # dict : 1 nom, 2: rank
        if order_choice == '1':
            players_list = sorted(
                players_list,
                key=lambda player: (player.name, player.surname)
            )
        # Ranking
        else:
            players_list = sorted(
                players_list,
                key=lambda player: (player.rank)
            )

        players_info = [
            f'{player.name} {player.surname}' for player in players_list
        ]
        choice = self.report_view.players_report(players_info)

        return choice

    @sub_menu
    def tournament_report(self) -> str:
        """
        First display all tournament and ask for choice on follow up.
        """
        tournament = self.tournaments_list_choice(
            self.tournament_list()
        )
        if not tournament:
            return 'q'
        choice = self.report_view.menu_detail_tournament()
        report_option = {
            '1': self.players_report,
            '2': self.matchs_report,
            '3': self.rounds_report,
            'q': lambda quit: None,
        }
        report_option[choice](tournament)
        return choice

    def tournament_list(self):
        return self.tournament_database.list_tournaments()

    def tournaments_list_choice(self, tournament_list: List[Tournament]) -> Optional[Tournament]:
        """
        Diplays all Tournaments and return the users' choice
        """
        tournaments_list = tournament_list
        # We retrieve only the name and date for the view
        tournaments_info = [
            f'{tournament.name}  -  {tournament.date}' for tournament in tournaments_list
        ]
        tournament_choice = self.report_view.tournament_report(
            tournaments_info
        )
        if tournament_choice == 'q':
            return
        index = int(tournament_choice) - 1
        return tournaments_list[index]

    def players_list(self, tournament: Tournament) -> List[Player]:
        return tournament.players

    @sub_menu
    def players_report(self, tournament: Tournament) -> str:
        """
        Displays all players name and surname from a given tournament.
        """
        players_list = self.sort_players(
            self.players_list(tournament)
        )
        # We retrieve only the name and surname for the view
        players_info = [
            f'{player.name} {player.surname}' for player in players_list]

        choice = self.report_view.players_report(players_info)

        return choice

    def sort_players(self, players: List[Player]):
        order_choice = self.report_view.report_sort_choice()
        # Alphabétique
        if order_choice == '1':
            players_list = sorted(
                players,
                key=lambda player: (player.name, player.surname)
            )
        # Ranking
        else:
            players_list = sorted(
                players,
                key=lambda player: (player.rank)
            )

        return players_list

    def matchs_list(self, tournament: Tournament) -> List[Match]:
        """
        Fetchs Matchs from a given tournament.
        Matchs are not stored in database.
        So we fetch the rounds from given tournament
        and create a list with all their respective matchs
        """
        rounds = self.rounds_list(tournament)
        match_list = []
        for round_ in rounds:
            match_list.extend(round_.matchs)

        return match_list

    @sub_menu
    def matchs_report(self, tournament: Tournament) -> None:
        """
        Displays Matchs from a given tournament.
        """
        matchs = self.matchs_list(tournament)
        choice = self.report_view.match_report(matchs)

        return choice

    def rounds_list(self, tournament: Tournament) -> List[Round]:
        """
        Fetchs Rounds from a given tournament.
        """
        return tournament.rounds

    @sub_menu
    def rounds_report(self, tournament: Tournament) -> str:
        """
        Displays all the rounds from a given tournament
        """
        rounds = self.rounds_list(tournament)
        round_lists = [
            f'{round.name} : {round.start_round_time}  --  {round.end_round_time}' for round in rounds
        ]
        choice = self.report_view.round_report(round_lists)
        return choice


class TournamentController:
    def __init__(self, view: View, report_controller: ReportController) -> None:
        self.view = view
        self.tournament_db = table_factory('tournaments')
        self.player_db = table_factory('players')
        self.report_controller = report_controller

    @sub_menu
    def run(self) -> str:
        if not hasattr(self, 'tournament') or not self.tournament:
            return self.initiate_tournament()

        if self.remaining_round > 0:
            choice = self.game_menu()
        else:
            self.end_tournament()
            choice = 'q'

        return choice

    def end_tournament(self) -> None:
        """
        Update the players rank according to their score and ranking.
        Displays the ranking for the user.
        """
        self.sort_players()

        player_list = []
        for index, player in enumerate(self.tournament.players):
            player.update_rank(index + 1)
            player_list.append(
                f'{player.rank}. {player.name} {player.surname} : {player.score}'
            )

        self.view.display_ranking(player_list)

        self.tournament = None

    @sub_menu
    def game_menu(self) -> str:
        if self.remaining_round <= 0:
            return 'q'
        choice = self.view.game_menu()
        choices = {
            '1': self.launch_round,
            '2': self.update_player_rank,
            'q': lambda: None,
        }
        choices[choice]()
        return choice

    def launch_round(self) -> None:
        self.create_round()

        self.play_matchs()

        for match in self.round.matchs:
            self.enter_score(match)
        self.remaining_round -= 1

        self.save_tournament(
            {
                'rounds': self.tournament.rounds
            },
            self.tournament.id,
        )

    def update_player_rank(self) -> None:
        player_list = self.report_controller.players_list(
            self.tournament
        )
        players_info = [
            f'{player.name} {player.surname} - rank : {player.rank}' for player in player_list]

        choice = self.report_controller.report_view.players_report(
            players_info)
        if choice == 'q':
            return

        index = int(choice) - 1
        player = player_list[index]
        player_info = players_info[index]
        new_rank = self.view.update_player_rank(player_info)
        player.update_rank(new_rank)
        # prompt players
        # choose
        # update choice

    def save_tournament(self, data, tournament_id) -> None:
        if type(data) == dict:
            self.tournament_db.update_tournament(
                data,
                tournament_id,
            )
        else:
            self.tournament_db.create_tournament(data)

    @sub_menu
    def initiate_tournament(self) -> str:
        # Create tournament and players:
        choice = self.view.start_tournament()
        choices = {
            '1': self.create_tournament,
            '2': self.load_tournament,
            'q': lambda: True,
        }

        # When you want to quit or tournament succesfully loaded/created :
        if choices[choice]():
            return 'q'

        return choice

    def play_matchs(self) -> None:
        self.round.start_round()

        self.view.end_matchs()

        self.round.end_round()

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

    def sort_players(self) -> None:
        """
        At the beginning of each round, we sort the players
        according to their score.
        When the tournament end, we sort again before displaying final ranking.
        If two players have the same score,
        we use their rank.
        """
        players_list = list(reversed(
            sorted(
                self.tournament.players,
                key=(lambda player: (player.score, player.rank))
            )
        ))
        self.tournament.players = players_list

    def load_tournament(self) -> bool:
        """
        Fetchs all unfinished tournament and makes the user choose
        one tournament.
        Return False if impossible.
        """
        tournament_list = self.report_controller.tournament_list()

        unfinished_tournament = []
        for tournament in tournament_list:
            # rounds are created only when the previous is over.
            if not tournament.rounds[-1].end_round_time or tournament.nbr_round != len(tournament.rounds):
                unfinished_tournament.append(tournament)

        self.tournament = self.report_controller.tournaments_list_choice(
            unfinished_tournament
        )

        if not self.tournament:
            return False

        # Since rounds are created one at a time, the remaining rounds don't exist yet.
        self.remaining_round = (
            self.tournament.nbr_round - len(self.tournament.rounds)
        )

        # Round can be created but not played yet :
        if not self.tournament.rounds[-1].end_round_time:
            self.remaining_round += 1

        return True

    def create_tournament(self) -> bool:
        tournament_info = self.view.get_tournament_info()
        tournament = Tournament(
            tournament_info['name'],
            tournament_info['place'],
            tournament_info['date'],
            tournament_info['description'],
        )
        self.tournament = tournament
        self.remaining_round = self.tournament.nbr_round

        nbr_player = tournament_info['nbr_player']

        # Player
        for _ in range(nbr_player):
            self.tournament.add_player(
                self.create_player()
            )

        self.tournament_db.create_tournament(tournament)

        return True

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

        self.player_db.create_player(player)
        return player

    def create_round(self) -> None:
        # Check if round already created before but not played :
        if not self.tournament.rounds[-1].end_round_time:
            self.round = self.tournament.rounds[-1]
            return

        round_info = self.view.get_round_info()

        # Match
        self.sort_players()
        match_list = self.create_matchs()

        self.round = Round(
            round_info['name'],
            match_list
        )

        self.tournament.add_round(
            self.round
        )
        self.save_tournament(
            {
                'rounds': self.tournament.rounds,
            },
            self.tournament.id
        )

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


class MainController:
    def __init__(
        self,
        view: View,
        tournament_controller: TournamentController,
        report_controller: ReportController,
    ) -> None:
        self.view = view
        self.tournament_controller = tournament_controller
        self.report_controller = report_controller

    def run(self) -> None:
        self.view.start_programm()
        self.main_prompt()
        self.view.end_programm()

    @sub_menu
    def main_prompt(self) -> str:
        choice = self.view.main_menu()
        choices = {
            '1': self.tournament_controller.run,
            '2': self.report_controller.run,
            'q': lambda: None,
        }
        choices[choice]()
        return choice


# if __name__ == '__main__':
#     view = View()
#     controller = TournamentController(view)
#     # controller.run()
#     players_list = [
#         Player('Pointud', 'Patrick', 'birthdate', 'gender', 4),
#         Player('Sanika', 'Florent', 'birthdate', 'gender', 1),
#         Player('Pointud', 'Émilie', 'birthdate', 'gender', 2),
#         Player('Sanika', 'Nathan', 'birthdate', 'gender', 3),
#         Player('Boyer', 'Marie-Huguette', 'birthdate', 'gender', 6),
#         Player('Pointud', 'Magdeline', 'birthdate', 'gender', 5),
#         Player('Sanika', 'Johvani', 'birthdate', 'gender', 8),
#         Player('Sanika', 'Marina', 'birthdate', 'gender', 7),
#     ]

#     # controller.tournament = Tournament(
#     #     'Tournament',
#     #     'place',
#     #     'date',
#     #     'description',
#     # )

#     # for player in players:
#     #     controller.tournament.add_player(player)

#     # for i in range(controller.tournament.nbr_round):
#     #     print(f'Tour {i+1} : ')
#     #     controller.sort_players()
#     #     controller.create_round()
#     #     controller.play_matchs()
#     #     for match in controller.round.matchs:
#     #         controller.enter_score(match)
#     #     print(controller.round)

#     report_controller = ReportController()
#     report_controller.players_report(players_list)

#     # tournament = controller.create_tournament()
#     # print(tournament)

#     # player = controller.create_player()
#     # print(player.__dict__)
