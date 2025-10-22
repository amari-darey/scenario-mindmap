from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtCore import Qt, QPointF
from core.edge import EdgeItem
from core.node import NodeItem

class NodeService:
    def __init__(self, scene, view, parent=None):
        self.scene = scene
        self.view = view
        self.parent = parent

    def create_child(self, node):
        pos = node.pos() + QPointF(180, 0)
        child = NodeItem('New node')
        child.setPos(pos)
        return child

    def start_edit(self, node):
        node.text_item.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextEditorInteraction |
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        node.text_item.setFocus()

    def change_color(self, node):
        c = QColorDialog.getColor(node.color, self.parent or self.view, 'Select node color')
        if c.isValid():
            node.setColor(c)

    def delete_node(self, node):
        for e in list(node.edges):
            self.scene.removeItem(e)
            try:
                e.source.removeEdge(e); e.dest.removeEdge(e)
            except Exception:
                pass
        self.scene.removeItem(node)
