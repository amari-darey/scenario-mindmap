from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QTransform

from core.node import NodeItem
from core.edge import EdgeItem


class MindMapScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_selected = None

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), QTransform())
        if isinstance(item, NodeItem):
            self.first_node_for_connect = item
        super().mousePressEvent(event)