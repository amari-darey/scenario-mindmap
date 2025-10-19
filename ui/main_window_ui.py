from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QDockWidget, 
    QTabWidget, QTextEdit, QVBoxLayout, 
    QLabel, QPushButton, QFontComboBox, 
    QSpinBox, QCheckBox, QHBoxLayout
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class MainWindowUI:
    def __init__(self, main_window: QMainWindow):
        main_window = main_window
        self._create_main_window(main_window)
        self._create_menubar(main_window)
        self._create_sidebar(main_window)
        self._create_toolbar(main_window)
        self._create_info_bar(main_window)

    def _create_main_window(self, main_window):
        main_window.setWindowTitle("scenarioMindMap")
        main_window.resize(1200, 800)
        self.placeholder_central = QWidget()
        main_window.setCentralWidget(self.placeholder_central)

    def _create_menubar(self, main_window):
        
        menubar = main_window.menuBar()

        file_menu = menubar.addMenu("&File")
        self.menubar_menu_module = menubar.addMenu("&Module")

        self.act_save = QAction("&Save", main_window)
        self.act_load = QAction("&Load", main_window)

        file_menu.addAction(self.act_save)
        file_menu.addAction(self.act_load)

    def _create_sidebar(self, main_window):
        dock = QDockWidget("Node inspector", main_window)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)

        self.sidebar_tab = QTabWidget()

        note_widget = QWidget()
        note_layout = QVBoxLayout()
        self.note_label = QLabel("Note for selected node:")
        self.note_edit = QTextEdit()
        note_layout.addWidget(self.note_label)
        note_layout.addWidget(self.note_edit)
        note_widget.setLayout(note_layout)

        attr_widget = QWidget()
        self.attr_layout = QVBoxLayout()

        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        self.color_btn = QPushButton("Choose color")
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_btn)
        self.attr_layout.addLayout(color_layout)

        font_layout = QHBoxLayout()
        font_label = QLabel("Font:")
        self.font_combo = QFontComboBox()
        self.font_size = QSpinBox()
        self.font_size.setRange(6, 72)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        font_layout.addWidget(self.font_size)
        self.attr_layout.addLayout(font_layout)

        style_layout = QHBoxLayout()
        self.bold_chk = QCheckBox("Bold")
        self.italic_chk = QCheckBox("Italic")
        style_layout.addWidget(self.bold_chk)
        style_layout.addWidget(self.italic_chk)
        self.attr_layout.addLayout(style_layout)

        self.apply_attr_btn = QPushButton("Apply to selected")
        self.attr_layout.addWidget(self.apply_attr_btn)
        self.attr_layout.addStretch(1)
        attr_widget.setLayout(self.attr_layout)

        self.sidebar_tab.addTab(note_widget, "Note")
        self.sidebar_tab.addTab(attr_widget, "Attributes")
        dock.setWidget(self.sidebar_tab)
        main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def _create_toolbar(self, main_window):
        self.toolbar = main_window.addToolBar("Tool Bar")
        self.toolbar.setOrientation(Qt.Orientation.Vertical)
        main_window.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        self.act_export = QAction("Export PNG", main_window)
        self.toolbar.addAction(self.act_export)
        self.toolbar.addSeparator()

    def _create_info_bar(self, main_window):
        self.info = main_window.statusBar()
