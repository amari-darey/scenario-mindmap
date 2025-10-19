from PyQt6.QtWidgets import QMainWindow

from controllers.main_window_adapter import MainWindowAdapter


class MainController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = MainWindowAdapter(self)
