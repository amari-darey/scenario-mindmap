from PyQt6.QtWidgets import QApplication
from controllers.main_controller import MainController
from controllers.project_selector_controller import ProjectSelectorController
import sys


def main(argv):
    app = QApplication(argv)
    controller = ProjectSelectorController()
    controller.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main(sys.argv))