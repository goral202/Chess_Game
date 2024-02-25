from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QColor, QTransform, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QMenu, QAction
from pawns.square import Square

class Bishop(QGraphicsItem):
    """
    Bishop class represents a bishop chess piece.

    Attributes:
    - x (int): X-coordinate of the bishop on the chessboard.
    - y (int): Y-coordinate of the bishop on the chessboard.
    - size (int): Size of the bishop.
    - color (str): Color of the bishop ('white' or 'black').
    - image (QPixmap): Image of the bishop.
    - buffx, buffy (int): Buffer for storing initial position.
    - removed_item (int): Indicates if an opponent's piece is removed during a move.

    Methods:
    - boundingRect(): Returns the bounding rectangle of the bishop.
    - paint(): Draws the bishop on the chessboard.
    - mousePressEvent(event): Handles mouse press events for selecting the bishop and checking possible moves.
    - is_valid_move(x, y): Checks if the move to the specified coordinates is valid for the bishop.
    - is_valid_move2(x, y): Checks if the move without capturing is valid for the bishop.
    - collides_with_pawn(x, y): Checks if the bishop collides with an opponent's pawn at the specified coordinates.
    - collides_with_opponent(x, y): Checks if the bishop collides with an opponent's piece at the specified coordinates.
    - remove_opponent(x, y): Removes an opponent's piece at the specified coordinates.
    - collides_with_pawns_on_the_way(x, y): Checks if there are pawns in the bishop's path to the target coordinates.
    - mouseReleaseEvent(event): Handles mouse release events for executing the bishop move.
    - move(x, y): Moves the bishop to the specified coordinates.
    - check_possible(): Highlights possible move locations for the bishop.
    - uncheck_possible(): Resets the highlighting of possible move locations.
    - update_board(): Displays a context menu for changing the chessboard colors.
    - set_board_color(color, color2, pawn): Changes the chessboard colors based on user selection.

    """
    def __init__(self, x, y, size, color, image_path):
        """
        Initialize the Bishop.

        Args:
        - x (int): Initial X-coordinate of the bishop.
        - y (int): Initial Y-coordinate of the bishop.
        - size (int): Size of the bishop.
        - color (str): Color of the bishop ('white' or 'black').
        - image_path (str): Path to the image of the bishop.

        """
        super().__init__()
        self.x = x
        self.y = y
        self.setPos(self.x, self.y)
        self.size = size
        self.color = color
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.image = QPixmap(image_path).scaled(self.size, self.size)
        self.buffx = x
        self.buffy = y
        self.removed_item = 0

    def boundingRect(self):
        """
        Returns the bounding rectangle of the bishop.

        Returns:
        - QRectF: Bounding rectangle of the bishop.

        """
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        """
        Draws the bishop on the chessboard.

        Args:
        - painter: The QPainter object to paint on.
        - option: Additional options for painting.
        - widget: The widget being painted.

        """
        rect = self.boundingRect()
        painter.drawPixmap(rect, self.image, QRectF())

    def mousePressEvent(self, event):
        """
        Handles mouse press events for selecting the bishop and checking possible moves.

        Args:
        - event: The mouse press event.

        """
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.offset = event.pos() - self.pos()
            self.check_possible()
        if event.button() == Qt.RightButton:
            update_board(self)

    def is_valid_move(self, x, y):
        """
        Checks if the move to the specified coordinates is valid for the bishop.

        Args:
        - x (int): Target X-coordinate.
        - y (int): Target Y-coordinate.

        Returns:
        - bool: True if the move is valid, False otherwise.

        """
        # Check if target coordinates are within the chessboard bounds
        if x < 0 or x > 960 or y < 0 or y > 960:
            return False

        dx = x - self.x
        dy = y - self.y
        # Check valid diagonal move
        if (abs(dy) / 120) == (abs(dx) / 120):
            # Check if there are no pawns on the way and captures an opponent's piece
            if not self.collides_with_pawns_on_the_way(x, y) and self.collides_with_opponent(x, y):
                return True
        return False

    def is_valid_move2(self, x, y):
        """
        Checks if the move without capturing is valid for the bishop.

        Args:
        - x (int): Target X-coordinate.
        - y (int): Target Y-coordinate.

        Returns:
        - bool: True if the move is valid, False otherwise.

        """
        # Check if target coordinates are within the chessboard bounds
        if x < 0 or x > 960 or y < 0 or y > 960:
            return False

        dx = x - self.x
        dy = y - self.y
        # Check valid diagonal move
        if (abs(dy) / 120) == (abs(dx) / 120):
            # Check if there are no pawns on the way
            if not self.collides_with_pawns_on_the_way(x, y):
                return True
        return False

    def collides_with_pawn(self, x, y):
        """
        Checks if the bishop collides with an opponent's pawn at the specified coordinates.

        Args:
        - x (int): X-coordinate to check.
        - y (int): Y-coordinate to check.

        Returns:
        - bool: True if collision with opponent's pawn, False otherwise.

        """
        for item in self.scene().items():
            if not isinstance(item, Square) and item.x == x and item.y == y and item.color != self.color:
                return True
        return False

    def collides_with_opponent(self, x, y):
        """
        Checks if the bishop collides with an opponent's piece at the specified coordinates.

        Args:
        - x (int): X-coordinate to check.
        - y (int): Y-coordinate to check.

        Returns:
        - bool: True if collision with opponent's piece, False otherwise.

        """
        for item in self.scene().items():
            if not isinstance(item, Square) and item.color != self.color and item.x == x and item.y == y:
                return True
            if not isinstance(item, Square) and item.color == self.color and item.x == x and item.y == y:
                return False
        return True

    def remove_opponent(self, x, y):
        """
        Removes an opponent's piece at the specified coordinates.

        Args:
        - x (int): X-coordinate to remove.
        - y (int): Y-coordinate to remove.

        Returns:
        - bool: True if an opponent's piece is removed, False otherwise.

        """
        for item in self.scene().items():
            if not isinstance(item, Square) and item.color != self.color and item.x == x and item.y == y:
                self.removed_item = item
                self.scene().removeItem(item)
                return True
            if not isinstance(item, Square) and item.color == self.color and item.x == x and item.y == y:
                self.removed_item = 0
                return False
        return True

    def collides_with_pawns_on_the_way(self, x, y):
        """
        Checks if there are pawns in the bishop's path to the target coordinates.

        Args:
        - x (int): Target X-coordinate.
        - y (int): Target Y-coordinate.

        Returns:
        - bool: True if there are pawns in the path, False otherwise.

        """
        dx = x - self.x
        dy = y - self.y
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1
        xt, yt = self.x + sx * 120, self.y + sy * 120
        i = 0
        while x != xt and y != yt:
            for item in self.scene().items():
                i += 1
                if not isinstance(item, Square) and item.x == xt and item.y == yt:
                    return True
            xt += sx * 120
            yt += sy * 120
            if i > 256:
                break
        return False

    def mouseReleaseEvent(self, event):
        """
        Handles mouse release events for executing the bishop move.

        Args:
        - event: The mouse release event.

        """
        super().mouseReleaseEvent(event)
        self.uncheck_possible()
        if event.button() == Qt.LeftButton:
            if self.isSelected():
                square = self.scene().itemAt(event.scenePos(), QTransform())
                if self.is_valid_move(square.x, square.y):
                    self.remove_opponent(square.x, square.y)
                    x = square.x + self.size / 2
                    y = square.y + self.size / 2
                    self.setPos(x - self.size / 2, y - self.size / 2)
                    self.x = x - self.size / 2
                    self.y = y - self.size / 2
                    if self.color == 'white':
                        if self.scene().check_white():
                            self.setPos(self.buffx, self.buffy)
                            self.x = self.buffx
                            self.y = self.buffy
                            if self.removed_item != 0:
                                self.scene().addItem(self.removed_item)
                        else:
                            self.buffx = self.x
                            self.buffy = self.y
                            if self.scene().current_turn == 'white':
                                self.scene().current_turn = 'black'
                            else:
                                self.scene().current_turn = 'white'
                    else:
                        if self.scene().check_black():
                            self.setPos(self.buffx, self.buffy)
                            self.x = self.buffx
                            self.y = self.buffy
                            if self.removed_item != 0:
                                self.scene().addItem(self.removed_item)
                        else:
                            self.buffx = self.x
                            self.buffy = self.y
                            if self.scene().current_turn == 'white':
                                self.scene().current_turn = 'black'
                            else:
                                self.scene().current_turn = 'white'
                self.setSelected(False)
            else:
                self.setSelected(True)
        elif event.button() == Qt.RightButton:
            self.scene().removeItem(self)
        else:
            self.setSelected(False)

    def move(self, x, y):
        """
        Moves the bishop to the specified coordinates.

        Args:
        - x (int): Target X-coordinate.
        - y (int): Target Y-coordinate.

        """
        square = self.scene().itemAt(QPoint(x, y), QTransform())
        if self.is_valid_move(square.x, square.y):
            self.remove_opponent(square.x, square.y)
            x = square.x + self.size / 2
            y = square.y + self.size / 2
            self.setPos(x - self.size / 2, y - self.size / 2)
            self.x = x - self.size / 2
            self.y = y - self.size / 2
            if self.color == 'white':
                if self.scene().check_white():
                    self.setPos(self.buffx, self.buffy)
                    self.x = self.buffx
                    self.y = self.buffy
                    if self.removed_item != 0:
                        self.scene().addItem(self.removed_item)
                else:
                    self.buffx = self.x
                    self.buffy = self.y
                    if self.scene().current_turn == 'white':
                        self.scene().current_turn = 'black'
                    else:
                        self.scene().current_turn = 'white'
            else:
                if self.scene().check_black():
                    self.setPos(self.buffx, self.buffy)
                    self.x = self.buffx
                    self.y = self.buffy
                    if self.removed_item != 0:
                        self.scene().addItem(self.removed_item)
                else:
                    self.buffx = self.x
                    self.buffy = self.y
                    if self.scene().current_turn == 'white':
                        self.scene().current_turn = 'black'
                    else:
                        self.scene().current_turn = 'white'

    def check_possible(self):
        """
        Highlights possible move locations for the bishop.

        """
        for item in self.scene().items():
            if isinstance(item, Square) and self.is_valid_move(item.x, item.y):
                item.color = QColor(102, 255, 102)
                item.update()

    def uncheck_possible(self):
        """
        Resets the highlighting of possible move locations.

        """
        for item in self.scene().items():
            if isinstance(item, Square) and self.is_valid_move(item.x, item.y):
                item.color = item.colorbuff
                item.update()

    def update_board(self):
        """
        Displays a context menu for changing the chessboard colors.

        """
        menu = QMenu(self.scene().views()[0])
        red_action = QAction('Yellow - Dark Blue', self.scene().views()[0])
        blue_action = QAction('White - Light Gray', self.scene().views()[0])
        green_action = QAction('Blue - Dark Blue', self.scene().views()[0])
        yellow_action = QAction('Yellow - Red', self.scene().views()[0])
        menu.addAction(red_action)
        menu.addAction(blue_action)
        menu.addAction(green_action)
        menu.addAction(yellow_action)
        red_action.triggered.connect(lambda: set_board_color('yellow', 'darkBlue', self))
        blue_action.triggered.connect(lambda: set_board_color('white', 'lightGray', self))
        green_action.triggered.connect(lambda: set_board_color('blue', 'darkBlue', self))
        yellow_action.triggered.connect(lambda: set_board_color('yellow', 'red', self))
        cursor_pos = QCursor.pos()
        menu.exec_(self.scene().views()[0].mapToGlobal(cursor_pos))

def set_board_color(color, color2, pawn):
    """
    Changes the chessboard colors based on user selection.

    Args:
    - color (str): Color for squares with pos=0.
    - color2 (str): Color for squares with pos!=0.
    - pawn: The bishop object.

    """
    for item in pawn.scene().items():
        if isinstance(item, Square):
            if item.pos == 0:
                item.color = QColor(color)
                item.colorbuff = QColor(color)
            else:
                item.color = QColor(color2)
                item.colorbuff = QColor(color2)
            item.update()
