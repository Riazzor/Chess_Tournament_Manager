from math import ceil, log
from functions import is_date_format, is_positive_number, menu_title, window_width


class View:
    def __init__(self) -> None:
        pass

    @menu_title('warning')
    def message(self, msg: str) -> None:
        """
        Used to send a message to the user.
        """
        if len(msg) <= window_width - 10:
            msg = ('/!\\'.center(5) + msg + '/!\\'.center(5))
        print(msg.center(window_width))

    def start_programm(self) -> None:
        print('=' * window_width)
        print('Bonjour'.center(window_width))
        print('Lancement du programme'.center(window_width))
        print('=' * window_width)

    def end_programm(self) -> None:
        print('=' * window_width)
        print(
            'Fin du programme'.center(window_width),
            'Bonne journée.'.center(window_width),
            sep='\n'
        )
        print('=' * window_width)

    @menu_title('Menu principal')
    def main_menu(self):
        options = {
            '1': 'Commencez un tournoi',
            '2': 'Affichez les rapports',
            'q': 'Quitter'
        }
        menu = ''
        for index, text in options.items():
            menu += f'{index}. {text}\n'
        menu += '\t-> '
        option = input(menu)
        while option not in ('1', '2', 'q'):
            print('Choisissez parmis 1/2/q')
            option = input(menu)
        return option

    @menu_title('Aucun tournoi de chargé')
    def start_tournament(self) -> str:
        options = {
            '1': 'Créer un nouveau tournoi',
            '2': 'Charger un tournoi existant',
            'q': 'Quitter',
        }
        menu = ''
        for index, text in options.items():
            menu += f'{index}. {text}\n'
        menu += '\t-> '

        option = input(menu)
        while option not in ('1', '2', 'q'):
            print('Choisissez parmis 1/2/q')
            option = input(menu)
        return option

    @menu_title('Menu tournoi')
    def game_menu(self) -> str:
        options = {
            '1': 'Lancer la ronde',
            '2': "Mettre à jour le rang d'un joueur",
            'q': 'Quitter'
        }
        menu = ''
        for index, text in options.items():
            menu += f'{index}. {text}\n'
        menu += '\t-> '
        option = input(menu)
        while option not in ('1', '2', 'q'):
            print('Choisissez parmis 1/2/q')
            option = input(menu)
        return option

    @menu_title('Classement des joueurs')
    def display_score(self, player_list: list):
        for player in player_list:
            print(player)

    def update_rank(self):
        response = '0'
        while response.lower() not in 'on':
            response = input('Voulez-vous mettre à jour le rang des joueurs (o/n)?') or '0'

        return {
            'o': 1,
            'n': 0,
        }[response.lower()]

    def update_player_rank(self, player_info: str, current_rank: int = -1) -> int:
        print(player_info)
        new_rank = input('Entrez le nouveau classement du joueur : ') or str(current_rank)
        while not is_positive_number(new_rank):
            new_rank = input('Entrez un nombre positif : ') or str(current_rank)
        return int(new_rank)

    @menu_title('Information du tournoi')
    def get_tournament_info(self) -> dict:
        print('Entrez les informations du tournoi :')
        name = input('Nom du tournoi : ')
        place = input('Emplacement : ')
        date = input('Date du tournoi (jj/mm/aaaa): ')
        while not is_date_format(date):
            date = input('Attention au format (jj/mm/aaaa): ')
        description = input('Description :\n')
        nbr_players = input('Nombre de joueur : ')
        while not is_positive_number(nbr_players):
            nbr_players = input('Entier positif : ')

        # According to the swiss system, number of round is found
        # using the binary logarithm of the number of player :
        default_rounds = str(ceil(
            log(int(nbr_players), 2)
        ))
        nbr_rounds = input(
            f'Nombre de tours ({default_rounds}): ') or default_rounds
        while not is_positive_number(nbr_rounds):
            nbr_rounds = input('Entier positif : ') or default_rounds

        time_menu = '1. Bullet\n'
        time_menu += '2. Blitz\n'
        time_menu += '3. Coup rapide'
        time_menu += '\n\t-> '
        time_control = input(f'Contrôle du temps: \n{time_menu}') or '0'
        while time_control not in '123':
            time_control = input(time_menu) or '0'

        tournament_information = {
            'name': name,
            'place': place,
            'date': date,
            'description': description,
            'nbr_players': nbr_players,
            'nbr_rounds': nbr_rounds,
            'time_control': time_control,
        }

        return tournament_information

    @menu_title('Information du joueur')
    def get_player_info(self, default_score='0') -> dict:
        name = input('Nom du joueur : ')
        surname = input('Prénom du joueur : ')
        birthdate = input('Date de naissance du joueur (JJ/MM/AAAA) : ')
        while not is_date_format(birthdate):
            birthdate = input('Attention au format (JJ/MM/AAAA) : ')
        gender = input('Genre du joueur (H/F) : ').upper()
        while gender not in ('H', 'F'):
            gender = input('H ou F : ').upper()
        rank = input('Classement général du joueur : ')
        while not is_positive_number(rank):
            rank = input('Entier positif : ')
        score = input(
            'Entrez le score du joueur (0 par défaut) : '
        )
        if not is_positive_number(score):
            score = default_score

        player_information = {
            'name': name,
            'surname': surname,
            'birthdate': birthdate,
            'gender': gender,
            'rank': rank,
            'score': score,
        }

        return player_information

    @menu_title('Information de la ronde')
    def get_round_info(self) -> dict:
        name = input('Nom de la ronde : ')
        round_information = {
            'name': name,
        }

        return round_information

    def end_matchs(self, time_control) -> bool:
        print(f'Rappel : controle du temps pour ce tournoi = {time_control}')
        print('À la fin du tour, tapez "fin".')
        choice = ''
        while choice != 'fin':
            choice = input('Tapez "fin" : ').lower()
        return True

    def enter_match_winner(self, p1_name, p2_name) -> int:  # 1 or 2 or 3
        """
            1.   Joueur 1
            2.   Joueur 2
            3.   Égalité
        """

        print(f'Match : {p1_name}, {p2_name}')
        print('Qui a gagné le match ? ')
        choice = ''
        while choice not in ('1', '2', '3'):
            choice = input(
                f"1.\t{p1_name}\n2.\t{p2_name}\n3.\tÉgalité\nChoix :    "
            )

        return choice


class ReportView:

    @menu_title('Menu des rapports')
    def main_menu(self) -> str:
        menu = '1. Rapport joueurs\n'
        menu += '2. Rapport tournois\n'
        menu += 'q. Quitter\n\t-> '
        choice = input(menu)
        while choice not in ('1', '2', 'q'):
            print('Choisissez entre 1/2/q')
            choice = input(menu)

        return choice

    def menu_detail_tournament(self):
        menu = '1. Liste des joueurs du tournoi\n'
        menu += '2. Liste des matchs du tournoi\n'
        menu += '3. Liste des tours du tournoi\n'
        menu += 'q. Retour au menu précédent.\n\t-> '
        choice = input(menu)
        while choice not in ('1', '2', '3', 'q'):
            print('Choisissez entre 1/2/3/q')
            choice = input(menu)

        return choice

    def report_sort_choice(self) -> str:
        print('Dans quel ordre voulez-vous votre rapport :')
        choice = ''
        while choice not in ('1', '2'):
            choice = input('1. Alphabétique \n2. Classement\n\t-> ')

        return choice

    @menu_title('Liste des joueurs')
    def players_report(self, player_list: list) -> str:
        """
        List of current tournament's players.
        Return the user's choosen player.
        """
        print('Selectionnez un joueur pour modification ou q pour quitter :\n')
        choice_index = [
            str(index) for index in range(1, len(player_list) + 1)
        ]
        player_menu = [
            f'{index}. {player} \n' for index, player in zip(choice_index, player_list)
        ]
        choice_index.append('q')
        player_menu.append(
            'q. Retour au menu précédent.'
        )
        possible_choice = '/'.join(choice_index)
        player_menu = ''.join(player_menu)
        player_menu += '\n\t-> '

        player_choice = input(player_menu)
        while player_choice not in choice_index:
            player_choice = input(
                f'Choisissez entre ({possible_choice})\n\t-> '
            )

        return player_choice

    @menu_title('Liste des tours')
    def round_report(self, rounds: list) -> str:
        """
        List of current tournament's rounds.
        """
        for index, round in enumerate(rounds, 1):
            print(f'{index}. {round}')

        # No other choice possible yet in this report.
        return 'q'

    @menu_title('Liste des matchs')
    def match_report(self, matchs: list) -> str:
        """
        List of current tournament's matchs.
        """
        for index, match in enumerate(matchs, 1):
            print(f'{index}. {match}')

        # No other choice possible yet in this report.
        return 'q'

    @menu_title('Liste des tournois')
    def tournament_report(self, tournament_list) -> str:
        """
        Displays the given tournament list.
        Users choose one of the tournament and the
        choice is returned.
        """
        choice_index = [
            str(index) for index in range(1, len(tournament_list) + 1)
        ]
        tournament_menu = [
            f'{index}. {tournament} \n' for index, tournament in zip(choice_index, tournament_list)
        ]
        choice_index.append('q')
        tournament_menu.append(
            'q. Retour au menu précédent.'
        )
        possible_choice = '/'.join(choice_index)
        tournament_menu = ''.join(tournament_menu)
        tournament_menu += '\n\t-> '

        tournament_choice = input(tournament_menu)
        while tournament_choice not in choice_index:
            tournament_choice = input(
                f'Choisissez entre ({possible_choice})\n\t-> '
            )

        return tournament_choice


if __name__ == '__main__':
    good_date = '10/12/2022'
    bad_dates = ['', 'aze', 'az/78/8858', '78945/7/8',
                 '-5', '12/13/2022', '32/15/2020']
    for date in bad_dates:
        assert is_date_format(date) is False, date

    assert is_date_format(good_date) is True, good_date

    view = ReportView()
    choice = view.tournament_report(
        [
            'Paris Game  -  05/03/2022',
            'London Game  -  05/04/2022',
            'Moscow Game  -  05/05/2022',
            'Berlin Game  -  05/06/2022',
        ]
    )
    print(choice)
