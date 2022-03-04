import re


def is_date_format(input_date) -> bool:
    """
    This function check that the input is a date so we
    can use datetime on the input.
    """
    date_pattern = re.compile(r'^(\d{2})\/(\d{2})\/(\d{4})$')

    good_date = date_pattern.fullmatch(input_date)
    if good_date:
        day, month, year = [int(group) for group in good_date.groups()]
        if 0 < day < 32 and 0 < month < 13 and 1900 < year < 2025:
            return True
    return False


class View:
    def __init__(self) -> None:
        pass

    def prompt_choice(self):
        options = {
            '1': 'Commencez un tournoi',
            '2': 'Affichez les rapports',
            '3': 'Quitter'
        }
        menu = ''
        for index, text in options.items():
            menu += f'{index}. {text}\n'
        option = ''
        while option not in ('1', '2', '3'):
            option = input()
        return option

    def get_tournament_info(self) -> dict:
        print('Entrez les informations du tournoi :')
        name = input('Nom du tournoi : ')
        place = input('Emplacement : ')
        date = ''
        while not is_date_format(date):
            date = input('Date du tournoi (jj/mm/aaaa): ')
        description = input('Description :\n')
        tournament_information = {
            'name': name,
            'place': place,
            'date': date,
            'description': description,
        }

        return tournament_information

    def get_player_info(self, default_score=0) -> dict:
        print('===================\nEntrez les informations du joueur :')

        name = input('Nom du joueur : ')
        surname = input('Prénom du joueur : ')
        birthdate = ''
        while not is_date_format(birthdate):
            birthdate = input('Date de naissance du joueur : ')
        gender = input('Genre du joueur : ')
        rank = input('Classement général du joueur : ')
        score = input(
            'Entrez le score du joueur (0 par défaut) : '
        ) or default_score

        player_information = {
            'name': name,
            'surname': surname,
            'birthdate': birthdate,
            'gender': gender,
            'rank': rank,
            'score': score,
        }

        return player_information

    def get_round_info(self) -> dict:
        print('Entrez les informations de la ronde :')
        name = input('Nom de la ronde : ')
        round_information = {
            'name': name,
        }

        return round_information

    def start_matchs(self, round_nbr) -> bool:
        print(f'Commencer le round {round_nbr} ?')
        choice = ''
        while choice not in ('o', 'n'):
            choice = input(' O/N : ').lower()
        if choice == 'n':
            return False
        return True

    def end_matchs(self) -> bool:
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

    def main_menu(self) -> str:
        menu = '1. Rapport joueurs\n'
        menu += '2. Rapport tournois\n'
        menu += '3. Quitter\n\t-> '
        choice = input(menu)
        while choice not in ('1', '2', '3'):
            print('Choisissez entre 1/2/3')
            choice = input(menu)

        return choice

    def menu_detail_tournament(self):
        menu = '1. Liste des joueurs du tournoi\n'
        menu += '2. Liste des matchs du tournoi\n'
        menu += '3. Liste des tours du tournoi\n'
        menu += '4. Retour menu précédent.\n\t-> '
        choice = input(menu)
        while choice not in ('1', '2', '3', '4'):
            print('Choisissez entre 1/2/3/4')
            choice = input(menu)

        return choice

    def report_sort_choice(self) -> str:
        print('Dans quel ordre voulez-vous votre rapport :')
        choice = ''
        while choice not in ('1', '2'):
            choice = input('1. Alphabétique \n2. Classement ')

        return choice

    def players_report(self, players: list) -> None:
        """
        List of current tournament's players.
        """
        for player in players:
            print(player)

    def round_report(self, rounds: list):
        for round in rounds:
            print(round)

        return None

    def match_report(self, matchs: list) -> None:
        for match in matchs:
            print(match)

        return None

    def tournament_report(self, tournament_list) -> int:
        """
        Displays the given tournament list.
        Users choose one of the tournament and the
        choice is returned.
        """
        choice_index = (
            str(index) for index in range(1, len(tournament_list) + 1)
        )
        tournament_menu = [
            f'{index}. {tournament} \n' for index, tournament in zip(choice_index, tournament_list)
        ]
        possible_choice = '/'.join(choice_index)
        tournament_menu = ''.join(tournament_menu)
        tournament_menu += '\n\t-> '

        tournament_choice = input(tournament_menu)
        while tournament_choice not in choice_index:
            tournament_choice = input(
                f'Choisissez entre ({possible_choice})\n\t-> ')

        return int(tournament_choice)


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
