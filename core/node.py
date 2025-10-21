
import uuid
from PyQt6.QtWidgets import QGraphicsObject, QGraphicsTextItem
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import QRectF, pyqtSignal, Qt

class NodeItem(QGraphicsObject):
    moved = pyqtSignal()

    def __init__(self, text='Node', width=160, height=80, color=QColor(255,255,200), uid=None, note='', font_family=None, font_size=None):
        super().__init__()
        self.uid = uid or str(uuid.uuid4())
        self.rect = QRectF(-width/2, -height/2, width, height)
        self.color = color
        self.note = note
        self.text_item = QGraphicsTextItem(self)
        self.text_item.setPlainText(text)
        self.text_item.setTextWidth(self.rect.width() - 10)
        self.text_item.setDefaultTextColor(QColor(30,30,30))
        self.text_item.setPos(self.rect.left()+5, self.rect.top()+5)
        self.text_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        if font_family or font_size:
            font = self.text_item.font()
            if font_family:
                font.setFamily(font_family)
            if font_size:
                font.setPointSize(font_size)
            self.text_item.setFont(font)
        self.setFlags(self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.edges = set()

    def boundingRect(self):
        return self.rect.adjusted(-4,-4,4,4)

    def paint(self, painter, option, widget=None):
        pen = QPen(QColor(80,80,80))
        pen.setWidth(1)
        painter.setPen(pen)
        brush = QBrush(self.color if not self.isSelected() else QColor(200,230,255))
        painter.setBrush(brush)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.drawRoundedRect(self.rect, 12, 12)

    def mouseDoubleClickEvent(self, event):
        self.text_item.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextEditorInteraction | 
                Qt.TextInteractionFlag.TextSelectableByMouse | 
                Qt.TextInteractionFlag.TextSelectableByKeyboard
                )
        self.text_item.setFocus()
        event.accept()

    def itemChange(self, change, value):
        from PyQt6.QtWidgets import QGraphicsItem
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for e in self.edges:
                e.updatePosition()
            self.moved.emit()
        return super().itemChange(change, value)

    def addEdge(self, edge):
        self.edges.add(edge)

    def removeEdge(self, edge):
        self.edges.discard(edge)

    def setColor(self, color):
        self.color = color
        self.update()

    def to_dict(self):
        font = self.text_item.font()
        return {
            'id': self.uid,
            'text': self.text_item.toPlainText(),
            'x': self.pos().x(),
            'y': self.pos().y(),
            'width': self.rect.width(),
            'height': self.rect.height(),
            'color': [self.color.red(), self.color.green(), self.color.blue()],
            'note': self.note,
            'font_family': font.family(),
            'font_size': font.pointSize()
        }
