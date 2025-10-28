from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QHBoxLayout, 
    QFileDialog
)

import os


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New Project")
        self.setMinimumWidth(400)
        self.setModal(True)
        
        self.project_name = ""
        self.project_dir = ""
        
        self.create_ui()
        self.set_style()
        self.connect()

        self.create_button.setEnabled(False)
        self.name_edit.setFocus()

    def run(self) -> tuple:
        if self.exec() == QDialog.DialogCode.Accepted:
            self.project_name = self.name_edit.text().strip()
            self.project_dir = self.path_edit.text().strip()
            return self.project_name, self.project_dir
        return None, None

    def connect(self):
        self.browse_button.clicked.connect(self.browse_folder)
        self.name_edit.textChanged.connect(self.update_create_button)
        self.path_edit.textChanged.connect(self.update_create_button)
        self.create_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def create_ui(self):
        self.layout_main = QVBoxLayout(self)
        self.name_layout = QVBoxLayout()
        self.name_label = QLabel("Project Name:")
        self.name_edit = QLineEdit()

        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_edit)

        self.path_layout = QVBoxLayout()
        self.path_label = QLabel("Project Location:")

        self.path_widget_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.browse_button = QPushButton("Browse...")

        self.path_widget_layout.addWidget(self.path_edit, 1)
        self.path_widget_layout.addWidget(self.browse_button)

        self.path_layout.addWidget(self.path_label)
        self.path_layout.addLayout(self.path_widget_layout)

        self.buttons_layout = QHBoxLayout()
        self.create_button = QPushButton("Create")
        self.cancel_button = QPushButton("Cancel")

        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.create_button)

        self.layout_main.addLayout(self.name_layout)
        self.layout_main.addSpacing(15)
        self.layout_main.addLayout(self.path_layout)
        self.layout_main.addSpacing(20)
        self.layout_main.addLayout(self.buttons_layout)
    
    def set_style(self):
        self.name_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        self.name_edit.setPlaceholderText("Enter project name...")
        self.name_edit.setStyleSheet("padding: 8px; border: 1px solid #ddd; border-radius: 4px;")

        self.path_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        self.path_edit.setPlaceholderText("Select project folder...")
        self.path_edit.setStyleSheet("padding: 8px; border: 1px solid #ddd; border-radius: 4px;")

        self.browse_button.setStyleSheet("""
            QPushButton {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: grey;
            }
            QPushButton:hover {
                background: #8F8F8F;
            }
        """)

        self.create_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background: grey;
                color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #45a049;
            }
            QPushButton:disabled {
                background: #575757;
                color: #e8f5e8;
            }
        """)

        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: grey;
            }
            QPushButton:hover {
                background: #A04545;
            }
        """)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Project Folder",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.path_edit.setText(folder)

    def update_create_button(self):
        has_name = bool(self.name_edit.text().strip())
        has_path = bool(self.path_edit.text().strip())
        self.create_button.setEnabled(has_name and has_path)
