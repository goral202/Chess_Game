from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QPen, QFont
from PyQt5.QtWidgets import QGraphicsItem

class Square(QGraphicsItem):
    def __init__(self, x, y, size, color, pos):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.colorbuff = color
        self.pos = pos
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(self.x, self.y, self.size, self.size)

    def paint(self, painter, option, widget):
        rect = self.boundingRect()
        brush = QBrush(self.color)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.fillRect(rect, brush)
        painter.drawRect(rect)
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)

        if self.y == 7*self.size:
            font = QFont("Arial", 10, QFont.Bold)
            painter.setFont(font)
            col_char = chr(ord('a') + self.x // self.size)
            painter.drawText(rect.adjusted(5, 5, 0, 0), Qt.AlignLeft | Qt.AlignTop, col_char)

        if self.x == 0:
            font = QFont("Arial", 10, QFont.Bold)
            painter.setFont(font)
            row_num = 8 - self.y // self.size
            painter.drawText(rect.adjusted(0, 0, -5, -5), Qt.AlignRight | Qt.AlignBottom, str(row_num))


