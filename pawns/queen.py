from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QColor, QTransform, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QMenu, QAction
from pawns.square import Square

class Queen(QGraphicsItem):
    """
    Queen class represents the queen chess piece on the board.

    Attributes:
    - x (int): X-coordinate of the queen.
    - y (int): Y-coordinate of the queen.
    - size (int): Size of the queen chess piece.
    - color (str): Color of the queen ('white' or 'black').
    - image (QPixmap): Image of the queen.
    - buffx, buffy (int): Buffers for the queen's position.
    - removed_item (QGraphicsItem): Item removed from the board during the move.

    Methods:
    - boundingRect(): Return the bounding rectangle of the queen.
    - paint(painter, option, widget): Paint the queen on the board.
    - mousePressEvent(event): Handle mouse press events for the queen.
    - is_valid_move(x, y): Check if the move to the given coordinates is valid.
    - is_valid_move2(x, y): Additional check for move validity.
    - collides_with_opponent(x, y): Check if the queen collides with an opponent at the given coordinates.
    - remove_opponent(x, y): Remove opponent's piece from the board at the given coordinates.
    - collides_with_pawns_on_the_way_rook(x, y): Check if there are pawns on the way for rook-like moves.
    - collides_with_pawns_on_the_way_bishop(x, y): Check if there are pawns on the way for bishop-like moves.
    - mouseReleaseEvent(event): Handle mouse release events for the queen.
    - move(x, y): Move the queen to the specified coordinates.
    - check_possible(): Check and highlight possible moves for the queen.
    - uncheck_possible(): Remove highlights from possible moves.
    """

    def __init__(self, x, y, size, color, image_path):
        """
        Initialize the Queen.

        Parameters:
        - x (int): X-coordinate of the queen.
        - y (int): Y-coordinate of the queen.
        - size (int): Size of the queen chess piece.
        - color (str): Color of the queen ('white' or 'black').
        - image_path (str): Path to the image file for the queen.

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
        Return the bounding rectangle of the queen.

        Returns:
        - QRectF: Bounding rectangle of the queen.

        """
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        """
        Paint the queen on the board.

        Parameters:
        - painter: QPainter object for painting.
        - option: QStyleOptionGraphicsItem specifying the style options.
        - widget: QWidget being painted on.

        """
        rect = self.boundingRect()
        painter.drawPixmap(rect, self.image, QRectF())

    def mousePressEvent(self, event):
        """
        Handle mouse press events for the queen.

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
                # Valid moves for white queen
                if abs(dy) > 0 and dx == 0:
                    if not self.collides_with_pawns_on_the_way_rook(x, y) and self.collides_with_opponent(x, y):
                        return True
                if abs(dx) > 0 and dy == 0:
                    if not self.collides_with_pawns_on_the_way_rook(x, y) and self.collides_with_opponent(x, y):
                        return True
                if (abs(dy) / 120) == (abs(dx) / 120):
                    if not self.collides_with_pawns_on_the_way_bishop(x, y) and self.collides_with_opponent(x, y):
                        return True
        if self.scene().current_turn == 'black':
            if self.color == 'black':
                # Valid moves for black queen
                if abs(dy) > 0 and dx == 0:
                    if not self.collides_with_pawns_on_the_way_rook(x, y) and self.collides_with_opponent(x, y):
                        return True
                if abs(dx) > 0 and dy == 0:
                    if not self.collides_with_pawns_on_the_way_rook(x, y) and self.collides_with_opponent(x, y):
                        return True
                if (abs(dy) / 120) == (abs(dx) / 120):
                    if not self.collides_with_pawns_on_the_way_bishop(x, y) and self.collides_with_opponent(x, y):
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
            # Additional checks for white queen's moves
            if abs(dy) > 0 and dx == 0:
                if not self.collides_with_pawns_on_the_way_rook(x, y) and self.collides_with_opponent(x, y):
                    return True
            if abs(dx) > 0 and dy == 0:
                if not self.collides_with_pawns_on_the_way_rook(x, y) and self.collides_with_opponent(x, y):
                    return True
            if (abs(dy) / 120) == (abs(dx) / 120):
                if not self.collides_with_pawns_on_the_way_bishop(x, y) and self.collides_with_opponent(x, y):
                    return True
        if self.color == 'black':
            # Additional checks for black queen's moves
            if abs(dy) > 0 and dx == 0:
                if not self.collides_with_pawns_on_the_way_rook(x, y) and self.collides_with_opponent(x, y):
                    return True
            if abs(dx) > 0 and dy == 0:
                if not self.collides_with_pawns_on_the_way_rook(x, y) and self.collides_with_opponent(x, y):
                    return True
            if (abs(dy) / 120) == (abs(dx) / 120):
                if not self.collides_with_pawns_on_the_way_bishop(x, y) and self.collides_with_opponent(x, y):
                    return True

        return False

    def collides_with_opponent(self, x, y):
        """
        Check if the queen collides with an opponent at the given coordinates.

        Parameters:
        - x (int): X-coordinate to check for collision.
        - y (int): Y-coordinate to check for collision.

        Returns:
        - bool: True if there is a collision with an opponent, False otherwise.

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
        - x (int): X-coordinate of the opponent's piece.
        - y (int): Y-coordinate of the opponent's piece.

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

    def collides_with_pawns_on_the_way_rook(self, x, y):
        """
        Check if there are pawns on the way for rook-like moves.

        Parameters:
        - x (int): Target x-coordinate for the move.
        - y (int): Target y-coordinate for the move.

        Returns:
        - bool: True if there are pawns on the way, False otherwise.

        """
        if self.x == x:
            start = self.y + 120 if self.y < y else y + 120
            end = y - 120 if self.y < y else self.y - 120
            for item in self.scene().items():
                if not isinstance(item, Square) and item.x == self.x and start <= item.y <= end:
                    return True
        else:
            start = self.x + 120 if self.x < x else x + 120
            end = x - 120 if self.x < x else self.x - 120
            for item in self.scene().items():
                if not isinstance(item, Square) and item.y == self.y and start <= item.x <= end:
                    return True

        return False

    def collides_with_pawns_on_the_way_bishop(self, x, y):
        """
        Check if there are pawns on the way for bishop-like moves.

        Parameters:
        - x (int): Target x-coordinate for the move.
        - y (int): Target y-coordinate for the move.

        Returns:
        - bool: True if there are pawns on the way, False otherwise.

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
            if i > 512:
                break
        return False

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events for the queen.

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
        Move the queen to the specified coordinates.

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
        Check and highlight possible moves for the queen.

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
    Update the board with a context menu for changing board colors.

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
    
    # Connect actions to set_board_color function
    red_action.triggered.connect(lambda: set_board_color('yellow', 'darkBlue', self))
    blue_action.triggered.connect(lambda: set_board_color('white', 'lightGray', self))
    green_action.triggered.connect(lambda: set_board_color('blue', 'darkBlue', self))
    yellow_action.triggered.connect(lambda: set_board_color('yellow', 'red', self))

    # Show the menu at the cursor position
    cursor_pos = QCursor.pos()
    menu.exec_(self.scene().views()[0].mapToGlobal(cursor_pos))

def set_board_color(color, color2, pawn):
    """
    Set the new color of the board.

    Parameters:
    - color (str): Color for squares with pos == 0.
    - color2 (str): Color for squares with pos != 0.
    - pawn (Queen): Queen pawn object.

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