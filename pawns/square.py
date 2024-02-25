from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QPen, QFont
from PyQt5.QtWidgets import QGraphicsItem

class Square(QGraphicsItem):
    """
    Square class represents a square on the chessboard.

    Attributes:
    - x (int): X-coordinate of the square.
    - y (int): Y-coordinate of the square.
    - size (int): Size of the square.
    - color (QColor): Color of the square.
    - colorbuff (QColor): Buffered color of the square.
    - pos (int): Position identifier for the square (0 or 1).
    
    Methods:
    - boundingRect(): Return the bounding rectangle of the square.
    - paint(painter, option, widget): Paint the square on the chessboard.

    """
    def __init__(self, x, y, size, color, pos):
        """
        Initialize the Square.

        Parameters:
        - x (int): X-coordinate of the square.
        - y (int): Y-coordinate of the square.
        - size (int): Size of the square.
        - color (QColor): Color of the square.
        - pos (int): Position identifier for the square (0 or 1).

        """
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.colorbuff = color
        self.pos = pos
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        """
        Return the bounding rectangle of the square.

        Returns:
        - QRectF: Bounding rectangle of the square.

        """
        return QRectF(self.x, self.y, self.size, self.size)

    def paint(self, painter, option, widget):
        """
        Paint the square on the chessboard.

        Parameters:
        - painter: QPainter object for painting.
        - option: QStyleOptionGraphicsItem specifying the style options.
        - widget: QWidget being painted on.

        """
        rect = self.boundingRect()
        brush = QBrush(self.color)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.fillRect(rect, brush)
        painter.drawRect(rect)
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)

        if self.y == 7 * self.size:
            font = QFont("Arial", 10, QFont.Bold)
            painter.setFont(font)
            col_char = chr(ord('a') + self.x // self.size)
            painter.drawText(rect.adjusted(5, 5, 0, 0), Qt.AlignLeft | Qt.AlignTop, col_char)

        if self.x == 0:
            font = QFont("Arial", 10, QFont.Bold)
            painter.setFont(font)
            row_num = 8 - self.y // self.size
            painter.drawText(rect.adjusted(0, 0, -5, -5), Qt.AlignRight | Qt.AlignBottom, str(row_num))