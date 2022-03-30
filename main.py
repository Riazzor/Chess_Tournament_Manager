from controllers import MainController, TournamentController, ReportController
from views import View


view = View()

report_controller = ReportController()
tournament_controller = TournamentController(view, report_controller)
main_controller = MainController(view, tournament_controller, report_controller)

main_controller.run()
