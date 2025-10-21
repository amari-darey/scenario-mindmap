from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QTransform

from core.edge import EdgeItem


class MindMapScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.first_node_for_connect = None
        self.connect_mode = False

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), QTransform())
        if self.connect_mode and isinstance(item, object):
            if self.first_node_for_connect is None:
                self.first_node_for_connect = item
                item.setSelected(True)
            else:
                if item is not self.first_node_for_connect:
                    edge = EdgeItem(self.first_node_for_connect, item)
                    self.addItem(edge)
                self.first_node_for_connect.setSelected(False)
                self.first_node_for_connect = None
            return
        super().mousePressEvent(event)