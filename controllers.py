from typing import List, Optional
from functions import sub_menu, table_factory
from models import Match, Player, Round, Tournament
from random import choice as random_choice
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

        choice = self.game_menu()

        return choice

    def end_tournament(self) -> None:
        """
        Update the players rank according to their score and ranking.
        Displays the ranking for the user.
        """
        self.sort_players()

        players_list = []
        for index, player in enumerate(self.tournament.players, 1):
            # player.update_rank(index)
            players_list.append(
                f'{player.rank}. {player.name} {player.surname} finale score : {player.score}'
            )

        self.view.display_score(players_list)
        if self.view.update_rank():
            self.update_all_player_rank()

        self.tournament = None

    @sub_menu
    def game_menu(self) -> str:
        if self.remaining_round <= 0:
            self.end_tournament()
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
        players_list = list(self.tournament.players)
        players_info = [
            f'{player.name} {player.surname} - rank : {player.rank}' for player in players_list]

        choice = self.report_controller.report_view.players_report(
            players_info)
        if choice == 'q':
            return

        index = int(choice) - 1
        player = players_list[index]
        player_info = players_info[index]

        new_rank = self.view.update_player_rank(player_info, player.rank)
        player.update_rank(new_rank)

        for player in Player.players_instance:
            self.save_player(
                {
                    'rank': player.rank,
                },
                player.id
            )
        # breakpoint()

    def update_all_player_rank(self):
        player_list = self.tournament.players

        for player in player_list:
            player_info = f'{player.name} {player.surname} - rank : {player.rank}'
            new_rank = self.view.update_player_rank(player_info, player.rank)
            player.update_rank(new_rank)

        for player in player_list:
            self.save_player(
                {
                    'rank': player.rank,
                },
                player.id
            )

    def save_tournament(self, data, tournament_id=None) -> None:
        if type(data) == dict:
            self.tournament_db.update_tournament(
                data,
                tournament_id,
            )
        else:
            self.tournament_db.create_tournament(data)

    def save_player(self, data, player_id=None) -> None:
        if type(data) == dict:
            self.player_db.update_player(
                data,
                player_id,
            )
        else:
            self.player_db.create_player(data)

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

        self.view.end_matchs(self.tournament.time_control)

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

        for player in (player1, player2):
            data = {
                'score': player.score,
                'opponents': player.opponents,
            }
            self.save_player(data, player.id)

    def sort_players(self, reverse=True) -> None:
        """
        At the beginning of each round, we sort the players
        according to their score.
        When the tournament end, we sort again before displaying final ranking.
        If two players have the same score,
        we use their rank.
        """
        def key(player):
            if reverse:
                return (player.score, -1 * player.rank)
            return (player.score, player.rank)
        players_list = list(
            sorted(
                self.tournament.players,
                key=key,
                reverse=reverse,
            )
        )
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
            has_round = bool(tournament.rounds)
            has_unfinished_round = bool(
                has_round and not tournament.rounds[-1].end_round_time)
            has_remaining_round = bool(
                tournament.nbr_round != len(tournament.rounds))
            if has_unfinished_round or has_remaining_round:
                unfinished_tournament.append(tournament)

        if not unfinished_tournament:
            self.view.message('Aucun tournoi de commencé')
            return False

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
        if self.tournament.rounds and not self.tournament.rounds[-1].end_round_time:
            self.remaining_round += 1

        self.game_menu()

        return True

    def create_tournament(self) -> bool:
        tournament_info = self.view.get_tournament_info()
        time_control = {
            '1': 'Bullet',
            '2': 'Blitz',
            '3': 'Coup rapide',
        }
        tournament = Tournament(
            tournament_info['name'],
            tournament_info['place'],
            tournament_info['date'],
            tournament_info['description'],
            int(tournament_info['nbr_rounds']),
            time_control[
                tournament_info['time_control']
            ]
        )
        self.tournament = tournament
        self.remaining_round = self.tournament.nbr_round

        nbr_players = int(tournament_info['nbr_players'])

        # Player
        for _ in range(nbr_players):
            self.tournament.add_player(
                self.create_player()
            )

        # We need to save the players only when they are all created
        # for case where the players are not given in order
        for player in self.tournament.players:
            self.save_player(player)
        self.save_tournament(tournament)

        self.game_menu()

        return True

    def create_player(self) -> Player:
        player_info = self.view.get_player_info()
        player = Player(
            player_info['name'],
            player_info['surname'],
            player_info['birthdate'],
            player_info['gender'],
            int(player_info['rank']),
            float(player_info['score'])
        )

        return player

    def create_round(self) -> None:
        # Check if round already created before but not played :
        if self.tournament.rounds and not self.tournament.rounds[-1].end_round_time:
            self.round = self.tournament.rounds[-1]
            return

        round_info = self.view.get_round_info()

        # Match
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
        The list of player is split in
        two sublist (S1 and S2).
        The first of S1 plays against the first of S2,
        the second of S1 against the second of S2, and
        so on so that the last player of S1
        plays against the last player of S2.
        If the player already played against the opponents,
        he will play against the next in line.
        """
        matchs = []

        # 1st round :
        if self.remaining_round == self.tournament.nbr_round:
            self.sort_players(reverse=False)
            players_list = list(self.tournament.players)
            middle = len(players_list) // 2
            is_not_even = len(players_list) % 2
            firs_half, second_half = players_list[:middle], players_list[middle:]
            for player1, player2 in zip(firs_half, second_half):
                matchs.append(
                    Match(player1, player2)
                )
                player1.opponents.append(player2.id)
                player2.opponents.append(player1.id)

            # should not happen but this part handles an odd number of players :
            if is_not_even:
                # a random player will be choosed to play a second time.
                matchs.append(
                    Match(
                        players_list[-1],           # player1
                        random_choice(players_list[:-1])   # player2
                    )
                )

            return matchs

        # other rounds
        self.sort_players()
        players_to_match = list(self.tournament.players)
        while len(players_to_match):
            player = players_to_match.pop(0)

            # If player already played against everyone and the tournament is not over,
            # We wipe the opponents table
            if len(player.opponents) == len(self.tournament.players) - 1:
                player.opponents = []
            for index, challenger in enumerate(players_to_match):
                if challenger.id not in player.opponents:
                    player.opponents.append(challenger.id)
                    challenger.opponents.append(player.id)
                    players_to_match.pop(index)
                    break
            else:
                # If we get here, it means an odd number of player:
                # Swiss system says the lone player gets the point as if winning
                if not players_to_match:
                    player.score += 1
                    break
                # player didn't played against everyone but his remaining
                # opponents are already assigned
                else:
                    challenger = players_to_match.pop(0)

            matchs.append(
                Match(player, challenger)
            )

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
