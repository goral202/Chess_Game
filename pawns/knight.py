from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QColor, QTransform, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QMenu, QAction
from pawns.square import Square

class Knight(QGraphicsItem):
    """
    Knight class represents the knight chess piece on the board.

    Attributes:
    - x (int): X-coordinate of the knight.
    - y (int): Y-coordinate of the knight.
    - size (int): Size of the knight chess piece.
    - color (str): Color of the knight ('white' or 'black').
    - image (QPixmap): Image of the knight.
    - buffx, buffy (int): Buffers for the knight's position.
    - removed_item (QGraphicsItem): Item removed from the board during the move.

    Methods:
    - boundingRect(): Return the bounding rectangle of the knight.
    - paint(painter, option, widget): Paint the knight on the board.
    - mousePressEvent(event): Handle mouse press events for the knight.
    - is_valid_move(x, y): Check if the move to the given coordinates is valid.
    - is_valid_move2(x, y): Additional check for move validity.
    - collides_with_pawn(x, y): Check if the knight collides with a pawn at the given coordinates.
    - collides_with_opponent(x, y): Check if the knight collides with an opponent at the given coordinates.
    - remove_opponent(x, y): Remove opponent's piece from the board at the given coordinates.
    - collides_with_pawns_on_the_way(x, y): Check if there are pawns in the knight's path.
    - mouseReleaseEvent(event): Handle mouse release events for the knight.
    - move(x, y): Move the knight to the specified coordinates.
    - check_possible(): Check and highlight possible moves for the knight.
    - uncheck_possible(): Remove highlights from possible moves.
    """

    def __init__(self, x, y, size, color, image_path):
        """
        Initialize the Knight.

        Parameters:
        - x (int): X-coordinate of the knight.
        - y (int): Y-coordinate of the knight.
        - size (int): Size of the knight chess piece.
        - color (str): Color of the knight ('white' or 'black').
        - image_path (str): Path to the image file for the knight.

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
        Return the bounding rectangle of the knight.

        Returns:
        - QRectF: Bounding rectangle of the knight.

        """
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        """
        Paint the knight on the board.

        Parameters:
        - painter: QPainter object for painting.
        - option: QStyleOptionGraphicsItem specifying the style options.
        - widget: QWidget being painted on.

        """
        rect = self.boundingRect()
        painter.drawPixmap(rect, self.image, QRectF())

    def mousePressEvent(self, event):
        """
        Handle mouse press events for the knight.

        Parameters:
        - event: QMouseEvent object representing the mouse press event.

        """
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.offset = event.pos() - self.pos()
            self.check_possible()
        if event.button() == Qt.RightButton:
            update_board(self)

    def is_valid_move(self, x, y):
        """
        Check if the move to the given coordinates is valid.

        Parameters:
        - x (int): Target x-coordinate for the move.
        - y (int): Target y-coordinate for the move.

        Returns:
        - bool: True if the move is valid, False otherwise.

        """
        # Check if coordinates are within the board boundaries
        if x < 0 or x > 960 or y < 0 or y > 960:
            return False

        dx = x - self.x
        dy = y - self.y

        # Check valid moves based on the current turn and color
        if self.scene().current_turn == 'white':
            if self.color == 'white':
                # Valid moves for white knight
                if (abs(dy) / 120) == 2 and (abs(dx) / 120) == 1:
                    if self.collides_with_opponent(x, y):
                        return True
                if (abs(dy) / 120) == 1 and (abs(dx) / 120) == 2:
                    if self.collides_with_opponent(x, y):
                        return True

        if self.scene().current_turn == 'black':
            if self.color == 'black':
                # Valid moves for black knight
                if (abs(dy) / 120) == 2 and (abs(dx) / 120) == 1:
                    if self.collides_with_opponent(x, y):
                        return True
                if (abs(dy) / 120) == 1 and (abs(dx) / 120) == 2:
                    if self.collides_with_opponent(x, y):
                        return True

        return False

    def is_valid_move2(self, x, y):
        """
        Additional check for move validity.

        Parameters:
        - x (int): Target x-coordinate for the move.
        - y (int): Target y-coordinate for the move.

        Returns:
        - bool: True if the move is valid, False otherwise.

        """
        # Check if coordinates are within the board boundaries
        if x < 0 or x > 960 or y < 0 or y > 960:
            return False

        dx = x - self.x
        dy = y - self.y

        # Additional checks for knight's move validity
        if self.color == 'white':
            if (abs(dy) / 120) == 2 and (abs(dx) / 120) == 1:
                if self.collides_with_opponent(x, y):
                    return True
            if (abs(dy) / 120) == 1 and (abs(dx) / 120) == 2:
                if self.collides_with_opponent(x, y):
                    return True

        if self.color == 'black':
            if (abs(dy) / 120) == 2 and (abs(dx) / 120) == 1:
                if self.collides_with_opponent(x, y):
                    return True
            if (abs(dy) / 120) == 1 and (abs(dx) / 120) == 2:
                if self.collides_with_opponent(x, y):
                    return True

        return False

    def collides_with_pawn(self, x, y):
        """
        Check if the knight collides with a pawn at the given coordinates.

        Parameters:
        - x (int): Target x-coordinate for collision check.
        - y (int): Target y-coordinate for collision check.

        Returns:
        - bool: True if collision with opponent's pawn, False otherwise.

        """
        for item in self.scene().items():
            if not isinstance(item, Square) and item.x == x and item.y == y and item.color != self.color:
                return True
        return False

    def collides_with_opponent(self, x, y):
        """
        Check if the knight collides with an opponent at the given coordinates.

        Parameters:
        - x (int): Target x-coordinate for collision check.
        - y (int): Target y-coordinate for collision check.

        Returns:
        - bool: True if collision with opponent, False otherwise.

        """
        for item in self.scene().items():
            if not isinstance(item, Square) and item.color != self.color and item.x == x and item.y == y:
                return True
            if not isinstance(item, Square) and item.color == self.color and item.x == x and item.y == y:
                return False
        return True

    def remove_opponent(self, x, y):
        """
        Remove opponent's piece from the board at the given coordinates.

        Parameters:
        - x (int): Target x-coordinate for removal.
        - y (int): Target y-coordinate for removal.

        Returns:
        - bool: True if opponent's piece removed, False otherwise.

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
        Check if there are pawns in the knight's path.

        Parameters:
        - x (int): Target x-coordinate for path check.
        - y (int): Target y-coordinate for path check.

        Returns:
        - bool: True if there are pawns in the path, False otherwise.

        """
        dx = x - self.x
        dy = y - self.y
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1
        xt, yt = self.x + sx * 120, self.y + sy * 120
        while x != xt and y != yt:
            for item in self.scene().items():
                if not isinstance(item, Square) and item.x == xt and item.y == yt:
                    return True
            xt += sx * 120
            yt += sy * 120
        return False

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events for the knight.

        Parameters:
        - event: QMouseEvent object representing the mouse release event.

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

                    # Check and update turn and positions after the move
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
        Move the knight to the specified coordinates.

        Parameters:
        - x (int): Target x-coordinate for the move.
        - y (int): Target y-coordinate for the move.

        """
        square = self.scene().itemAt(QPoint(x, y), QTransform())
        if self.is_valid_move(square.x, square.y):
            self.remove_opponent(square.x, square.y)
            x = square.x + self.size / 2
            y = square.y + self.size / 2
            self.setPos(x - self.size / 2, y - self.size / 2)
            self.x = x - self.size / 2
            self.y = y - self.size / 2

            # Check and update turn and positions after the move
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
        Check and highlight possible moves for the knight.

        """
        for item in self.scene().items():
            if isinstance(item, Square) and self.is_valid_move(item.x, item.y):
                item.color = QColor(102, 255, 102)
                item.update()

    def uncheck_possible(self):
        """
        Remove highlights from possible moves.

        """
        for item in self.scene().items():
            if isinstance(item, Square) and self.is_valid_move(item.x, item.y):
                item.color = item.colorbuff
                item.update()

def update_board(self):
    """
    Update the board by showing a context menu to choose a new color.

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

    # Connect actions to set_board_color function with different parameters
    red_action.triggered.connect(lambda: set_board_color('yellow', 'darkBlue', self))
    blue_action.triggered.connect(lambda: set_board_color('white', 'lightGray', self))
    green_action.triggered.connect(lambda: set_board_color('blue', 'darkBlue', self))
    yellow_action.triggered.connect(lambda: set_board_color('yellow', 'red', self))

    # Show the menu at the cursor position
    cursor_pos = QCursor.pos()
    menu.exec_(self.scene().views()[0].mapToGlobal(cursor_pos))

def set_board_color(color, color2, pawn):
    """
    Set the new color for the chessboard.

    Parameters:
    - color (str): Primary color for the chessboard.
    - color2 (str): Secondary color for the chessboard.
    - pawn: Instance of the Knight class.

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