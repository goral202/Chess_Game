from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QColor, QTransform, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QMenu, QAction
from pawns.square import Square

class King(QGraphicsItem):
    """
    King class represents the king chess piece on the board.

    Attributes:
    - x (int): X-coordinate of the king.
    - y (int): Y-coordinate of the king.
    - size (int): Size of the king chess piece.
    - color (str): Color of the king ('white' or 'black').
    - image (QPixmap): Image of the king.
    - possible_move (list): List of possible moves for the king.
    - buffx, buffy (int): Buffers for the king's position.
    - removed_item (QGraphicsItem): Item removed from the board during the move.

    Methods:
    - boundingRect(): Return the bounding rectangle of the king.
    - paint(painter, option, widget): Paint the king on the board.
    - mousePressEvent(event): Handle mouse press events for the king.
    - is_valid_move(x, y): Check if the move to the given coordinates is valid.
    - is_valid_move2(x, y): Additional check for move validity.
    - check(x, y): Check if the king is in check at the given coordinates.
    - collides_with_opponent(x, y): Check if the king collides with an opponent at the given coordinates.
    - remove_opponent(x, y): Remove opponent's piece from the board at the given coordinates.
    - mouseReleaseEvent(event): Handle mouse release events for the king.
    - possible(x, y): Check if the move to the given coordinates is in the list of possible moves.
    - move(x, y): Move the king to the specified coordinates.
    - check_possible(): Check and highlight possible moves for the king.
    - uncheck_possible(): Remove highlights from possible moves.
    """

    def __init__(self, x, y, size, color, image_path):
        """
        Initialize the King.

        Parameters:
        - x (int): X-coordinate of the king.
        - y (int): Y-coordinate of the king.
        - size (int): Size of the king chess piece.
        - color (str): Color of the king ('white' or 'black').
        - image_path (str): Path to the image file for the king.

        """
        super().__init__()
        self.x = x
        self.y = y
        self.setPos(self.x, self.y)
        self.size = size
        self.color = color
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.image = QPixmap(image_path).scaled(self.size, self.size)
        self.possible_move = []
        self.buffx = x
        self.buffy = y
        self.removed_item = 0

    def boundingRect(self):
        """
        Return the bounding rectangle of the king.

        Returns:
        - QRectF: Bounding rectangle of the king.

        """
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        """
        Paint the king on the board.

        Parameters:
        - painter: QPainter object for painting.
        - option: QStyleOptionGraphicsItem specifying the style options.
        - widget: QWidget being painted on.

        """
        rect = self.boundingRect()
        painter.drawPixmap(rect, self.image, QRectF())

    def mousePressEvent(self, event):
        """
        Handle mouse press events for the king.

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
                # Valid moves for white king
                if abs(dy) / 120 == 1 and dx == 0:
                    if self.collides_with_opponent(x, y):
                        return True
                if abs(dx) / 120 == 1 and dy == 0:
                    if self.collides_with_opponent(x, y):
                        return True
                if (abs(dy) / 120) == (abs(dx) / 120) == 1:
                    if self.collides_with_opponent(x, y):
                        return True

        if self.scene().current_turn == 'black':
            if self.color == 'black':
                # Valid moves for black king
                if abs(dy) / 120 == 1 and dx == 0:
                    if self.collides_with_opponent(x, y):
                        return True
                if abs(dx) / 120 == 1 and dy == 0:
                    if self.collides_with_opponent(x, y):
                        return True
                if (abs(dy) / 120) == (abs(dx) / 120) == 1:
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

        if self.color == 'white':
            # Additional check for white king's move validity
            if abs(dy) / 120 == 1 and dx == 0:
                if self.collides_with_opponent(x, y):
                    return True
            if abs(dx) / 120 == 1 and dy == 0:
                if self.collides_with_opponent(x, y):
                    return True
            if (abs(dy) / 120) == (abs(dx) / 120) == 1:
                if self.collides_with_opponent(x, y):
                    return True

        if self.color == 'black':
            # Additional check for black king's move validity
            if abs(dy) / 120 == 1 and dx == 0:
                if self.collides_with_opponent(x, y):
                    return True
            if abs(dx) / 120 == 1 and dy == 0:
                if self.collides_with_opponent(x, y):
                    return True
            if (abs(dy) / 120) == (abs(dx) / 120) == 1:
                if self.collides_with_opponent(x, y):
                    return True

        return False

    def check(self, x, y):
        """
        Check if the king is in check at the given coordinates.

        Parameters:
        - x (int): Target x-coordinate for the check.
        - y (int): Target y-coordinate for the check.

        Returns:
        - bool: True if the king is in check, False otherwise.

        """
        for item in self.scene().items():
            if not isinstance(item, Square) and item.color != self.color:
                if item.is_valid_move2(x, y):
                    return True
        return False

    def collides_with_opponent(self, x, y):
        """
        Check if the king collides with an opponent at the given coordinates.

        Parameters:
        - x (int): Target x-coordinate for collision check.
        - y (int): Target y-coordinate for collision check.

        Returns:
        - bool: True if the king collides with an opponent, False otherwise.

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
        - bool: True if opponent's piece is removed, False otherwise.

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

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events for the king.

        Parameters:
        - event: QMouseEvent object representing the mouse release event.

        """
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            if self.isSelected():
                square = self.scene().itemAt(event.scenePos(), QTransform())
                if self.possible(square.x, square.y):
                    self.remove_opponent(square.x, square.y)
                    x = square.x + self.size / 2
                    y = square.y + self.size / 2
                    self.setPos(x - self.size / 2, y - self.size / 2)
                    self.x = x - self.size / 2
                    self.y = y - self.size / 2

                    if self.color == 'white':
                        self.scene().kingwpos = [self.x, self.y]
                    else:
                        self.scene().kingbpos = [self.x, self.y]

                    if self.color == 'white':
                        if self.scene().check_white():
                            self.setPos(self.buffx, self.buffy)
                            self.x = self.buffx
                            self.y = self.buffy
                            if self.removed_item != 0:
                                self.scene().addItem(self.removed_item)
                            self.scene().kingwpos = [self.scene().buffkingwpos[0], self.scene().buffkingwpos[0]]
                        else:
                            self.buffx = self.x
                            self.buffy = self.y
                            self.scene().buffkingwpos = [self.x, self.y]
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
                            self.scene().kingbpos = [self.scene().buffkingbpos[0], self.scene().buffkingbpos[0]]
                        else:
                            self.buffx = self.x
                            self.buffy = self.y
                            self.scene().buffkingbpos = [self.x, self.y]
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
        self.uncheck_possible()

    def possible(self, x, y):
        """
        Check if the move to the given coordinates is in the list of possible moves.

        Parameters:
        - x (int): Target x-coordinate for the move.
        - y (int): Target y-coordinate for the move.

        Returns:
        - bool: True if the move is possible, False otherwise.

        """
        for item in self.possible_move:
            if item.x == x and item.y == y:
                return True
        return False

    def move(self, x, y):
        """
        Move the king to the specified coordinates.

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
            if self.color == 'white':
                self.scene().kingwpos = [self.x, self.y]
            else:
                self.scene().kingbpos = [self.x, self.y]

            if self.color == 'white':
                if self.scene().check_white():
                    self.setPos(self.buffx, self.buffy)
                    self.x = self.buffx
                    self.y = self.buffy
                    if self.removed_item != 0:
                        self.scene().addItem(self.removed_item)
                    self.scene().kingwpos = [self.scene().buffkingwpos[0], self.scene().buffkingwpos[0]]
                else:
                    self.buffx = self.x
                    self.buffy = self.y
                    self.scene().buffkingwpos = [self.x, self.y]
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
                    self.scene().kingbpos = [self.scene().buffkingbpos[0], self.scene().buffkingbpos[0]]
                else:
                    self.buffx = self.x
                    self.buffy = self.y
                    self.scene().buffkingbpos = [self.x, self.y]
                    if self.scene().current_turn == 'white':
                        self.scene().current_turn = 'black'
                    else:
                        self.scene().current_turn = 'white'

    def check_possible(self):
        """
        Check and highlight possible moves for the king.

        """
        for item in self.scene().items():
            if isinstance(item, Square) and self.is_valid_move(item.x, item.y):
                if not self.check(item.x, item.y):
                    item.color = QColor(102, 255, 102)
                    self.possible_move.append(item)
                    item.update()

    def uncheck_possible(self):
        """
        Remove highlights from possible moves.

        """
        self.possible_move = []
        for item in self.scene().items():
            if isinstance(item, Square):
                item.color = item.colorbuff
                item.update()

def update_board(self):
    """
    Update the board colors based on the user's selection.

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

    # Connect actions to color setting functions
    red_action.triggered.connect(lambda: set_board_color('yellow', 'darkBlue', self))
    blue_action.triggered.connect(lambda: set_board_color('white', 'lightGray', self))
    green_action.triggered.connect(lambda: set_board_color('blue', 'darkBlue', self))
    yellow_action.triggered.connect(lambda: set_board_color('yellow', 'red', self))

    # Show the menu at the cursor position
    cursor_pos = QCursor.pos()
    menu.exec_(self.scene().views()[0].mapToGlobal(cursor_pos))

def set_board_color(color, color2, pawn):
    """
    Set the board colors based on the user's selection.

    Parameters:
    - color (str): Color for squares with pos=0.
    - color2 (str): Color for squares with pos=1.
    - pawn: The QGraphicsItem representing the pawn on the board.

    """
    # Set the new colors for the squares on the board
    for item in pawn.scene().items():
        if isinstance(item, Square):
            if item.pos == 0:
                item.color = QColor(color)
                item.colorbuff = QColor(color)
            else:
                item.color = QColor(color2)
                item.colorbuff = QColor(color2)
            item.update()
