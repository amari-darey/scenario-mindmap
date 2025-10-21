from PyQt6.QtWidgets import QMainWindow, QMenu
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QPointF

from controllers.main_window_adapter import MainWindowAdapter
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
        test_root = self.create_node('Root', QPointF(0,0))
        test_child = self.create_node('Child', QPointF(240,-120))
        self.scene.addItem(EdgeItem(test_root, test_child))

        self.view.contextMenuEvent = lambda event: self.menu_controller(event)


    def connect(self):
        ...

    def create_node(self, text, position=(0,0), color=QColor(255,255,200), uid=None, note='', font_family=None, font_size=None):
        pos = position if isinstance(position, QPointF) else QPointF(position[0], position[1])
        node = NodeItem(text, color=color, uid=uid, note=note, font_family=font_family, font_size=font_size)
        node.setPos(pos)
        node.setFlag(node.GraphicsItemFlag.ItemIsFocusable, True)
        self.scene.addItem(node)
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
        
    def scene_context_menu(self, pos, event_pos):
        menu = QMenu()
        add_child = menu.addAction('Add ellement')
        action = menu.exec(event_pos)
        if action == add_child:
            self.create_node('New node', position=pos)
