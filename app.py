from PyQt6.QtWidgets import QApplication
from controllers.main_controller import MainController
import sys


def main(argv):
    app = QApplication(argv)
    controller = MainController()
    controller.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main(sys.argv))