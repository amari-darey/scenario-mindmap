
from PyQt6.QtWidgets import QGraphicsPathItem
from PyQt6.QtGui import QPen, QColor, QPainterPath
from PyQt6.QtCore import QPointF

class EdgeItem(QGraphicsPathItem):
    def __init__(self, source, dest):
        super().__init__()
        self.source = source
        self.dest = dest
        pen = QPen(QColor(90,90,90))
        pen.setWidth(2)
        self.setPen(pen)
        self.setZValue(-1)
        source.addEdge(self)
        dest.addEdge(self)
        source.moved.connect(self.updatePosition)
        dest.moved.connect(self.updatePosition)
        self.updatePosition()

    def updatePosition(self):
        p1 = self.source.pos()
        p2 = self.dest.pos()
        path = QPainterPath()
        path.moveTo(p1)
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        c1 = QPointF(p1.x() + dx * 0.25, p1.y() + dy * 0.05)
        c2 = QPointF(p1.x() + dx * 0.75, p1.y() + dy * 0.95)
        path.cubicTo(c1, c2, p2)
        self.setPath(path)

    def to_dict(self):
        return {'source': self.source.uid, 'dest': self.dest.uid}