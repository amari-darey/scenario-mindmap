import json
import os
from PyQt6.QtWidgets import QMainWindow, QMenu, QColorDialog, QFileDialog, QMessageBox
from PyQt6.QtGui import QColor, QTextCursor
from PyQt6.QtCore import Qt, QPointF

import config
from controllers.main_window_adapter import MainWindowAdapter
from controllers.node_context_service import NodeService
from controllers.inspector_controller import InspectorController
from core.commands import CommandStack
from core.commands_node import AddNodeCommand, DeleteNodeCommand, AddEdgeCommand
from core.scene import MindMapScene
from core.view import MindMapView
from core.node import NodeItem
from core.edge import EdgeItem
from core.storage import JSONStorage
from core.info_manager import InfoManager

from constant import *


class MainController(QMainWindow):
    def __init__(self, project_name: str|bool = False, load_path: str|bool = False):
        super().__init__()
        self.ui = MainWindowAdapter(self)

        self.scene = MindMapScene(self)
        self.scene.setSceneRect(*SCENE_RECT)

        self.view = MindMapView(self.scene)

        self.setCentralWidget(self.view)

        self.command_stack = CommandStack()
        self.node_service = NodeService(self.scene, self.view, self)

        self.inspector = InspectorController(self.ui, self.scene, self.command_stack)

        self.info_manager = InfoManager(self.ui.info)

        self.project_name = project_name
        self.project_path = load_path

        self.app_func()
        self.connect()


    def app_func(self):
        self.view.contextMenuEvent = lambda event: self.menu_controller(event)

        if self.project_path:
            self.project_load(self.project_path)

    def connect(self):
        self.ui.act_undo.triggered.connect(self.command_stack.undo)
        self.ui.act_redo.triggered.connect(self.command_stack.redo)
        self.ui.act_save.triggered.connect(self.action_save_checker)
        self.ui.act_load.triggered.connect(self.action_load)

    def create_node(self, text, position=(0,0), color=QColor(255,255,200), uid=None, note="", font_family=None, font_size=None, font_color=None):
        pos = position if isinstance(position, QPointF) else QPointF(position[0], position[1])
        node = NodeItem(text, color=color, uid=uid, note=note, font_family=font_family, font_size=font_size, font_color=font_color)
        node.setPos(pos)
        node.setFlag(node.GraphicsItemFlag.ItemIsFocusable, True)
        return node
    
    def menu_controller(self, event):
        scene_pos = self.view.mapToScene(event.pos())
        item = self.scene.itemAt(scene_pos, self.view.transform())

        if isinstance(item, NodeItem):
            self.node_context_menu(item, event.globalPos())
        else:
            self.scene_context_menu(scene_pos, event.globalPos())

    def node_context_menu(self, node, event_pos):
        menu = QMenu()
        add_child = menu.addAction("Add child")
        edit_text = menu.addAction("Edit text")
        color_action = menu.addAction("Change color")
        font_color_action = menu.addAction("Change font color")
        delete_action = menu.addAction("Delete node")
        action = menu.exec(event_pos)

        if action == add_child:
            child_node = self.node_service.create_child(node)
            self.command_stack.push(AddNodeCommand(self.scene, child_node, node))

        elif action == edit_text:
            node.text_item.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextEditorInteraction | 
                Qt.TextInteractionFlag.TextSelectableByMouse | 
                Qt.TextInteractionFlag.TextSelectableByKeyboard
                )
            node.text_item.setFocus()

        elif action == color_action:
            color = QColorDialog.getColor(node.color, self, "Select node color")
            if color.isValid():
                node.setColor(color)

        elif action == font_color_action:
            color = QColorDialog.getColor(node.color, self, "Select node color")
            if color.isValid():
                node.text_item.setDefaultTextColor(color)

        elif action == delete_action:
            self.command_stack.push(DeleteNodeCommand(self.scene, node))
        
    def scene_context_menu(self, pos, event_pos):
        menu = QMenu()
        add_node = menu.addAction("Add ellement")
        action = menu.exec(event_pos)
        if action == add_node:
            new_node = self.create_node("New node", position=pos)
            self.command_stack.push(AddNodeCommand(self.scene, new_node))

    def action_save_checker(self):
        if os.path.exists(self.project_path):
            self.action_save(self.project_path)
        else:
            reply = QMessageBox.question(
                self,
                "Save file not found",
                "Do you want to save it somewhere else?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                path, _ = QFileDialog.getSaveFileName(self, 'Load MindMap', '', 'MindMap JSON (*.json)')
                self.action_save(path)
                self.recent_projects_edit(path)

    def recent_projects_edit(self, path):
        try:
            item = {}
            sorted_items = []
            data = {}

            with open(config.RECENT_PROJECTS_FILE_PATH, 'r', encoding='utf-8') as f:
                item = json.load(f)

            sorted_items = sorted(item.items(), key=lambda item: item[1]["time"])
            data = dict(sorted_items)
            data[self.project_name]["path"] = path

            with open(config.RECENT_PROJECTS_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"Error loading recent projects: {e}")


    def action_save(self, path):
        try:
            JSONStorage.save(path, self.scene)
            self.info_manager.send_message(f"Saved to {path}")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to save: {exc}")

    def action_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load MindMap", "", "MindMap JSON (*.json)")
        if not path:
            self.info_manager.send_error_message(f"No path to file")
            return
        try:
            JSONStorage.load(path, self.scene, create_node_fn=self._create_node_for_loader, create_edge_fn=self._create_edge_for_loader)
            self.project_path = path
            self.info_manager.send_message(f"Loaded {path}")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to load: {exc}")
        
    def project_load(self, path):
        try:
            JSONStorage.load(path, self.scene, create_node_fn=self._create_node_for_loader, create_edge_fn=self._create_edge_for_loader)
            self.info_manager.send_message(f"Loaded {path}")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to load: {exc}")
        
    def _create_node_for_loader(self, text, pos=(0,0), color=None, uid=None, note="", font_family=None, font_size=None, font_color=None):
        node = self.create_node(
                    text, 
                    position=pos, 
                    color=color or QColor(255,255,200), 
                    uid=uid, 
                    note=note, 
                    font_family=font_family, 
                    font_size=font_size,
                    font_color=font_color
                    )
        self.command_stack.push(AddNodeCommand(self.scene, node)) 
        return node
    
    def _create_edge_for_loader(self, scene, parent, child):
        self.command_stack.push(AddEdgeCommand(scene, parent, child))
