
from models import Tournament
from views import View


class Controller:
    def __init__(self, view) -> None:
        self.view = view

    def run(self):
        tournament = self.create_tournament()
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


if __name__ == '__main__':
    view = View()
    controller = Controller(view)
    # tournament = controller.create_tournament()
    # print(tournament)
