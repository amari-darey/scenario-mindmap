from core.edge import EdgeItem

from collections import deque

from config import command_stack_max_len


class Command:
    def do(self):
        raise NotImplementedError()
    def undo(self):
        raise NotImplementedError()


class CommandStack:
    def __init__(self):
        self._undo_stack = deque(maxlen=command_stack_max_len)
        self._redo_stack = deque(maxlen=command_stack_max_len)

    def push(self, cmd: Command):
        cmd.do()
        self._undo_stack.append(cmd)
        self._redo_stack.clear()

    def undo(self):
        if self._undo_stack:
            cmd = self._undo_stack.pop()
            cmd.undo()
            self._redo_stack.append(cmd)

    def redo(self):
        if self._redo_stack:
            cmd = self._redo_stack.pop()
            cmd.do()
            self._undo_stack.append(cmd)
