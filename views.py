class View:
    def __init__(self) -> None:
        pass

    def get_tournament_info(self) -> dict:
        print('Entrez les informations du tournoi')
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

    def get_player_info(self) -> dict:
        print('Entrez les informations du joueur:')
        player_information = {
            'name': input('Nom du joueur : '),
            'surname': input('Prénom du joueur : '),
            'birthdate': input('Date de naissance du joueur : '),
            'gender': input('Genre du joueur : '),
            'rank': input('Classement général du joueur : '),
            'score': 0
        }
        return player_information
