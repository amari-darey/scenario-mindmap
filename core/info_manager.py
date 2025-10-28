from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QStatusBar


class InfoManager:
    def __init__(self, info_widget: QStatusBar):
        self.info_widget = info_widget
        self.original_style = info_widget.styleSheet()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.restore_style)

    def send_message(self, text, timeout=3000):
        self.timer.stop()
        self.restore_style()
        self.info_widget.showMessage(text, timeout)

    def send_error_message(self, text, timeout=3000):
        self.timer.stop()
        self.info_widget.setStyleSheet("background-color: #ffcccc; color: #990000;")
        self.info_widget.showMessage(text, timeout)
        self.timer.start(timeout)

    def restore_style(self):
        self.info_widget.setStyleSheet(self.original_style)