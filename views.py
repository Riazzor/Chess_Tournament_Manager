class View:
    def __init__(self) -> None:
        pass

    def get_tournament_info(self) -> dict:
        print('Entrez les informations du tournoi :')
        name = input('Nom du tournoi : ')
        place = input('Emplacement : ')
        date = input('Date du tournoi : ')
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
        player_information = {
            'name': input('Nom du joueur : '),
            'surname': input('Prénom du joueur : '),
            'birthdate': input('Date de naissance du joueur : '),
            'gender': input('Genre du joueur : '),
            'rank': input('Classement général du joueur : '),
            'score': input('Entrez le score du joueur (0 par défaut) : ') or 0
        }

        return player_information

    def get_round_info(self) -> dict:
        print('Entrez les informations de la ronde :')
        name = input('Nom de la ronde : ')
        round_information = {
            'name': name,
        }

        return round_information

    def prompt_choice(self, option):
        options = {
            1: 'Tournoi',
            2: 'Quitter'
        }

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
