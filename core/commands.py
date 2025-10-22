from core.edge import EdgeItem


class Command:
    def do(self):
        raise NotImplementedError()
    def undo(self):
        raise NotImplementedError()


class CommandStack:
    def __init__(self):
        self._stack = []
        self._index = -1

    def push(self, cmd: Command):
        self._stack = self._stack[:self._index+1]
        cmd.do()
        self._stack.append(cmd)
        self._index += 1

    def undo(self):
        if self._index >= 0:
            cmd = self._stack[self._index]
            cmd.undo()
            self._index -= 1

    def redo(self):
        if self._index + 1 < len(self._stack):
            self._index += 1
            self._stack[self._index].do()


class AddNodeCommand(Command):
    def __init__(self, scene, node, parent_node=None):
        self.scene = scene 
        self.node = node
        self.parent_node = parent_node
        self.edge = None

    def do(self):
        self.scene.addItem(self.node)
        if self.parent_node:
            self.edge = EdgeItem(self.parent_node, self.node)
            self.scene.addItem(self.edge)
    def undo(self):
        if self.edge: 
            self.scene.removeItem(self.edge)
        self.scene.removeItem(self.node)
