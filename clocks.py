from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Clock(QWidget):
    """
    Clock class represents a simple clock widget.

    Attributes:
    - timer (QTimer): Timer for periodic updates.
    - time (int): Current time in milliseconds.
    - count (bool): Flag indicating whether the countdown is active.
    - hPointer, mPointer, sPointer, msPointer (QPolygon): Polygons representing hour, minute, second, and millisecond pointers.
    - bColor, sColor, msColor (QColor): Colors for pointers.
    - timer (QTimer): Timer for continuous updates.

    Methods:
    - count_down(): Decrement time and update widget.
    - paintEvent(event): Paint the clock widget.
    - mousePressEvent(event): Toggle countdown on mouse press.

    """

    def __init__(self):
        """
        Initialize the Clock widget.

        - Set up timers and initial properties.

        """
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.count_down)
        self.time = 5 * 60 * 1000
        self.count = True
        self.setWindowTitle('Clock')
        self.setGeometry(200, 200, 300, 300)
        self.setStyleSheet("background : white;")
        self.hPointer = QtGui.QPolygon([QPoint(6, 7), QPoint(-6, 7), QPoint(0, -50)])
        self.mPointer = QPolygon([QPoint(6, 7), QPoint(-6, 7), QPoint(0, -70)])
        self.sPointer = QPolygon([QPoint(1, 1), QPoint(-1, 1), QPoint(0, -90)])
        self.msPointer = QPolygon([QPoint(1, 1), QPoint(-1, 1), QPoint(0, -90)])
        self.bColor = Qt.black
        self.sColor = Qt.red
        self.msColor = Qt.blue

        self.timer.start(1)

    def count_down(self):
        """
        Decrement the time and update the widget.

        If counting, decrement the time. If the time reaches zero, stop the countdown.

        """
        if self.count:
            self.time -= 1
            if self.time <= 0:
                self.time = 0
                self.count = False

        self.update()

        


    def paintEvent(self, event):
        """
        Paint the clock widget.

        Draw the clock face, pointers, and scale.

        """
        rec = min(self.width(), self.height())

        painter = QPainter(self)

        def drawPointer(color, rotation, pointer):
            """
            Helper method to draw a pointer on the clock face.

            Parameters:
            - color: Color of the pointer.
            - rotation: Rotation angle for the pointer.
            - pointer: QPolygon defining the shape of the pointer.

            """
            painter.setBrush(QBrush(color))
            painter.save()
            painter.rotate(rotation)
            painter.drawConvexPolygon(pointer)
            painter.restore()

        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(rec / 200, rec / 200)
        painter.setPen(QtCore.Qt.NoPen)

        drawPointer(self.bColor, (30 * (self.time / (1000*60*60) % 12 + self.time / (1000*60) % 360 / 60)), self.hPointer)
        drawPointer(self.bColor, (6 * (self.time / (1000*60) % 360 + self.time / 1000 % 60 / 60)), self.mPointer)
        drawPointer(self.sColor, (6 * (self.time / 1000) % 360), self.sPointer)
        drawPointer(self.msColor, (360 * ((self.time % 1000) / 1000)), self.msPointer)



        painter.setPen(QPen(self.bColor))
        for i in range(0, 60):
            if (i % 5) == 0:
                painter.drawLine(87, 0, 97, 0)
            painter.rotate(6)

        painter.end()

    def mousePressEvent(self, event):
        """
        Toggle the countdown on mouse press.

        """
        if not self.count:
            self.count = True
        else:
            self.count = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Clock()
    win.show()
    sys.exit(app.exec_())
