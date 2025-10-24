from PyQt6.QtCore import Qt

from core.commands import Command
from core.edge import EdgeItem


class AddNodeCommand(Command):
    def __init__(self, scene, node, parent_node=None):
        self.scene = scene 
        self.node = node
        self.parent_node = parent_node
        self.edge = None

    def do(self):
        self.scene.addItem(self.node)
        if self.parent_node:
            self.__add_parrent_style()
            self.edge = EdgeItem(self.parent_node, self.node)
            self.scene.addItem(self.edge)

    def undo(self):
        if self.edge: 
            self.scene.removeItem(self.edge)
        self.scene.removeItem(self.node)

    def __add_parrent_style(self):
        self.node.setColor(self.parent_node.color)
        self.node.text_item.setDefaultTextColor(self.parent_node.text_item.defaultTextColor())


class AddEdgeCommand(Command):
    def __init__(self, scene, parent_note, node):
        self.scene = scene
        self.parent_note = parent_note
        self.node = node
        self.edge = None
    
    def do(self):
        self.edge = EdgeItem(self.parent_node, self.node)
        self.scene.addItem(self.edge)
    
    def undo(self):
        if self.edge: 
            self.scene.removeItem(self.edge)


class EditTextNodeCommand(Command):
    ...


class DeleteNodeCommand(Command):
    def __init__(self, scene, node):
        self.scene = scene
        self.node = node
        self.edges = []

    def do(self):
        for edge in list(self.node.edges):
            self.edges.append((edge.source, edge.dest))
            self.scene.removeItem(edge)
        self.scene.removeItem(self.node)

    def undo(self):
        self.scene.addItem(self.node)
        for s, d in self.edges:
            edge = EdgeItem(s, d)
            self.scene.addItem(edge)