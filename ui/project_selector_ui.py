from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QListWidget, 
    QSizePolicy
    )

import config


class ProjectSelectorUi:
    def __init__(self, main_window: QMainWindow):
        main_window = main_window
        self._create_main_window(main_window)
        self._create_selector(main_window)

    def _create_main_window(self, main_window):
        main_window.setWindowTitle("scenarioMindMap")
        main_window.resize(*config.project_selector_size)
        self.centralWidget = QWidget()
        main_window.setCentralWidget(self.centralWidget)

    def _create_selector(self, main_window):
        verticalLayout_main = QVBoxLayout()
        horizontalLayout_buttons = QHBoxLayout()
        label = QLabel("Choice map")
        self.listWidget_project = QListWidget()
        self.listWidget_project.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pushButton_open = QPushButton("Open")
        self.pushButton_create = QPushButton("Create")

        verticalLayout_main.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        verticalLayout_main.addWidget(self.listWidget_project)
        
        horizontalLayout_buttons.addWidget(self.pushButton_open, alignment=Qt.AlignmentFlag.AlignCenter)
        horizontalLayout_buttons.addWidget(self.pushButton_create, alignment=Qt.AlignmentFlag.AlignCenter)

        verticalLayout_main.addLayout(horizontalLayout_buttons)

        self.centralWidget.setLayout(verticalLayout_main)