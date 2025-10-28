from PyQt6.QtWidgets import QMainWindow, QFileDialog

from controllers.main_controller import MainController
from ui.project_selector_ui import ProjectSelectorUi
from core.project_selector_dialog import Dialog
import config

import os
import json
import time


class ProjectSelectorController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = ProjectSelectorUi(self)
        self.recent_projects = {}
        
        self._connect()
        self._setup()

    def _connect(self):
        self.ui.pushButton_open.clicked.connect(self._open_project)
        self.ui.pushButton_create.clicked.connect(self._create_new_project)

        self.ui.listWidget_project.itemDoubleClicked.connect(self._open_project)

    def _setup(self):
        self._load_recent_project()
        self._show_recent_projects()

    def _load_recent_project(self, event=False):
        try:
            if os.path.exists(config.RECENT_PROJECTS_FILE_PATH):
                with open(config.RECENT_PROJECTS_FILE_PATH, 'r', encoding='utf-8') as f:
                    self.recent_projects = json.load(f)
            else:
                with open(config.RECENT_PROJECTS_FILE_PATH, "w", encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False)
        except Exception as e:
            print(f"Error loading recent projects: {e}")

    def _save_project(self):
        try:
            sorted_items = sorted(self.recent_projects.items(), key=lambda item: item[1]["time"], reverse=True)
            data = dict(sorted_items)
            with open(config.RECENT_PROJECTS_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=f, indent=4)
        except Exception as e:
            print(f"Error loading recent projects: {e}")

    def _show_recent_projects(self):
        self.ui.listWidget_project.clear()
        for project in self.recent_projects:
            self.ui.listWidget_project.addItem(project)

    def _open_project(self):
        item = self.ui.listWidget_project.currentItem()
        if item:
            key = item.text()
            if key in self.recent_projects:
                path = self.recent_projects[key]
                self._update_time_on_project(key)
                self._launch_main_controller(key, path["path"])

    def _update_time_on_project(self, key):
        self.recent_projects[key]["time"] = int(time.time())

    def _create_new_project(self):
        dialog = Dialog()
        name, path = dialog.run()
        self.recent_projects[name] = {
            "path": f"{path}/{name}.json",
            "time": int(time.time())
            }
        with open(f"{path}/{name}.json", "w", encoding="utf-8") as file:
            json.dump({"nodes": [], "edges": []}, file, ensure_ascii=False)
        self._save_project()
        self._load_recent_project()
        self._show_recent_projects()
        
    def _launch_main_controller(self, project_name, project_path):
        self._save_project()
        self.main_controller = MainController(project_name, project_path)
        self.main_controller.show()
        self.close()
