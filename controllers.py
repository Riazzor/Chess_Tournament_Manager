
from models import Player, Tournament
from views import View


class Controller:
    def __init__(self, view) -> None:
        self.view = view

    def run(self):
        tournament = self.create_tournament()
        for _ in range(8):
            player = self.create_player()
            tournament.add_player(player)
        print(tournament)

    def create_tournament(self):
        tournament_info = self.view.get_tournament_info()
        tournament = Tournament(
            tournament_info['name'],
            tournament_info['place'],
            tournament_info['date'],
            tournament_info['description'],
        )
        return tournament

    def create_player(self):
        player_info = self.view.get_player_info()
        player = Player(
            player_info['name'],
            player_info['surname'],
            player_info['birthdate'],
            player_info['gender'],
            player_info['rank'],
            player_info['score']
        )
        return player


if __name__ == '__main__':
    view = View()
    controller = Controller(view)
    # tournament = controller.create_tournament()
    # print(tournament)

    player = controller.create_player()
    print(player.__dict__)
