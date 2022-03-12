from controllers import MainController, Controller, ReportController
from views import View


view = View()
tournament_controller = Controller(view)

report_controller = ReportController()
main_controller = MainController(view, tournament_controller, report_controller)

main_controller.run()
