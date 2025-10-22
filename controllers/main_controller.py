from PyQt6.QtWidgets import QMainWindow, QMenu
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QPointF

from controllers.main_window_adapter import MainWindowAdapter
from controllers.node_context_service import NodeService
from core.commands import AddNodeCommand, CommandStack
from core.scene import MindMapScene
from core.view import MindMapView
from core.node import NodeItem
from core.edge import EdgeItem

from constant import *


class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowAdapter(self)

        self.scene = MindMapScene(self)
        self.scene.setSceneRect(*SCENE_RECT)

        self.view = MindMapView(self.scene)

        self.setCentralWidget(self.view)

        self.app_func()
        self.connect()


    def app_func(self):
        self.command_stack = CommandStack()
        self.node_service = NodeService(self.scene, self.view, self)
        self.view.contextMenuEvent = lambda event: self.menu_controller(event)


    def connect(self):
        self.ui.act_undo.triggered.connect(self.command_stack.undo)
        self.ui.act_redo.triggered.connect(self.command_stack.redo)

    def create_node(self, text, position=(0,0), color=QColor(255,255,200), uid=None, note='', font_family=None, font_size=None):
        pos = position if isinstance(position, QPointF) else QPointF(position[0], position[1])
        node = NodeItem(text, color=color, uid=uid, note=note, font_family=font_family, font_size=font_size)
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
        add_child = menu.addAction('Add child')
        edit_text = menu.addAction('Edit text')
        color_action = menu.addAction('Change color')
        delete_action = menu.addAction('Delete node')
        action = menu.exec(event_pos)

        if action == add_child:
            child_node = self.node_service.create_child(node)
            self.command_stack.push(AddNodeCommand(self.scene, child_node, node))
        
    def scene_context_menu(self, pos, event_pos):
        menu = QMenu()
        add_node = menu.addAction('Add ellement')
        action = menu.exec(event_pos)
        if action == add_node:
            new_node = self.create_node('New node', position=pos)
            self.command_stack.push(AddNodeCommand(self.scene, new_node))
