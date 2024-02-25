from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QBrush, QColor, QPen, QFont, QTransform, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QDialog, QPushButton, QVBoxLayout, QGraphicsScene, QGraphicsView, QApplication, QMenu, QAction
from pawns.square import Square
from pawns.queen import Queen 
from pawns.rook import Rook 
from pawns.bishop import Bishop 
from pawns.knight import Knight 
from resource import *

wp = ':/wp.png'; bp=':/bp.png'; wr = ':/wr.png'; br = ':/br.png'; wn = ':/wn.png'; bn = ':/bn.png'; wb = ':/wb.png'; bb = ':/bb.png'; wk = ':/wk.png'; bk = ':/bk.png'; wq = ':/wq.png'; bq = ':/bq.png'

class Pawn(QGraphicsItem):
    """
    Pawn class represents a pawn chess piece on the board.

    Attributes:
    - x (int): X-coordinate of the pawn.
    - y (int): Y-coordinate of the pawn.
    - size (int): Size of the pawn chess piece.
    - color (str): Color of the pawn ('white' or 'black').
    - image (QPixmap): Image of the pawn.
    - first_move (bool): Flag indicating if it's the pawn's first move.
    - buffx, buffy (int): Buffers for the pawn's position.
    - removed_item (QGraphicsItem): Item removed from the board during the move.

    Methods:
    - boundingRect(): Return the bounding rectangle of the pawn.
    - paint(painter, option, widget): Paint the pawn on the board.
    - mousePressEvent(event): Handle mouse press events for the pawn.
    - is_valid_move(x, y): Check if the move to the given coordinates is valid.
    - is_valid_move2(x, y): Additional check for move validity.
    - collides_with_pawn(x, y): Check if the pawn collides with another pawn at the given coordinates.
    - collides_with_opponent(x, y): Check if the pawn collides with an opponent at the given coordinates.
    - remove_opponent(x, y): Remove opponent's piece from the board at the given coordinates.
    - collides_with_pawns_on_the_way(x, y): Check if there are pawns on the way during a double-step move.
    - mouseReleaseEvent(event): Handle mouse release events for the pawn.
    - move(x, y): Move the pawn to the specified coordinates.
    - check_possible(): Check and highlight possible moves for the pawn.
    - uncheck_possible(): Remove highlights from possible moves.
    """

    def __init__(self, x, y, size, color, image_path):
        """
        Initialize the Pawn.

        Parameters:
        - x (int): X-coordinate of the pawn.
        - y (int): Y-coordinate of the pawn.
        - size (int): Size of the pawn chess piece.
        - color (str): Color of the pawn ('white' or 'black').
        - image_path (str): Path to the image file for the pawn.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.setPos(self.x, self.y)
        self.size = size
        self.color = color
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.image = QPixmap(image_path).scaled(self.size, self.size)
        self.first_move = True
        self.buffx = x
        self.buffy = y
        self.removed_item = 0

    def boundingRect(self):
        """
        Return the bounding rectangle of the pawn.

        Returns:
        - QRectF: Bounding rectangle of the pawn.
        """
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        """
        Paint the pawn on the board.

        Parameters:
        - painter: QPainter object for painting.
        - option: QStyleOptionGraphicsItem specifying the style options.
        - widget: QWidget being painted on.
        """
        rect = self.boundingRect()
        painter.drawPixmap(rect, self.image, QRectF())

    def mousePressEvent(self, event):
        """
        Handle mouse press events for the pawn.

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

        if self.scene().current_turn == 'white':
            if self.color == 'white':
                if dy < 0:
                    return False

                if dy == 120:
                    if dx == 0 and not self.collides_with_pawn(x, y):
                        return True

                if dy == 240 and self.first_move and not self.collides_with_pawns_on_the_way(x, y):
                    if dx == 0 and not self.collides_with_pawn(x, y):
                        return True

                if abs(dy) == 120 and abs(dx) == 120 and self.collides_with_opponent(x, y):
                    return True

        if self.scene().current_turn == 'black':
            if self.color == 'black':
                if dy > 0:
                    return False

                if dy == -120:
                    if dx == 0 and not self.collides_with_pawn(x, y):
                        return True

                if dy == -240 and self.first_move:
                    if dx == 0 and not self.collides_with_pawn(x, y) and not self.collides_with_pawns_on_the_way(x, y):
                        return True

                if abs(dy) == 120 and abs(dx) == 120 and self.collides_with_opponent(x, y):
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
            if dy < 0:
                return False

            if abs(dy) == 120 and abs(dx) == 120:
                return True

        if self.color == 'black':
            if dy > 0:
                return False

            if abs(dy) == 120 and abs(dx) == 120:
                return True

        return False

    def collides_with_pawn(self, x, y):
        """
        Check if the pawn collides with another pawn at the given coordinates.

        Parameters:
        - x (int): x-coordinate to check for collision.
        - y (int): y-coordinate to check for collision.

        Returns:
        - bool: True if collision with another pawn, False otherwise.
        """
        for item in self.scene().items():
            if not isinstance(item, Square) and item.x == x and item.y == y:
                return True
        return False

    def collides_with_opponent(self, x, y):
        """
        Check if the pawn collides with an opponent at the given coordinates.

        Parameters:
        - x (int): x-coordinate to check for collision.
        - y (int): y-coordinate to check for collision.

        Returns:
        - bool: True if collision with an opponent, False otherwise.
        """
        for item in self.scene().items():
            if not isinstance(item, Square) and item.color != self.color and item.x == x and item.y == y:
                return True
        return False

    def remove_opponent(self, x, y):
        """
        Remove opponent's piece from the board at the given coordinates.

        Parameters:
        - x (int): x-coordinate to remove opponent's piece.
        - y (int): y-coordinate to remove opponent's piece.

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
        Check if there are pawns on the way during a double-step move.

        Parameters:
        - x (int): Target x-coordinate for the move.
        - y (int): Target y-coordinate for the move.

        Returns:
        - bool: True if there are pawns on the way, False otherwise.
        """
        if self.color == 'white':
            step = 120
        else:
            step = -120
        start = self.y + step
        end = y
        if start > end:
            start, end = end, start
        for item in self.scene().items():
            if not isinstance(item, Square) and item.x == self.x and start <= item.y <= end:
                return True
        return False

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events for the pawn.

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
                            self.first_move = False
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
                            self.first_move = False
                            if self.scene().current_turn == 'white':
                                self.scene().current_turn = 'black'
                            else:
                                self.scene().current_turn = 'white'

                    if self.y == 0 and self.color == 'black':
                        promote_pawn(self)
                    elif self.y == 840:
                        promote_pawn(self)

                self.setSelected(False)
            else:
                self.setSelected(True)
        elif event.button() == Qt.RightButton:
            self.scene().removeItem(self)
        else:
            self.setSelected(False)

    def move(self, x, y):
        """
        Move the pawn to the specified coordinates.

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
                    self.first_move = False
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
                    self.first_move = False
                    if self.scene().current_turn == 'white':
                        self.scene().current_turn = 'black'
                    else:
                        self.scene().current_turn = 'white'

            if self.y == 0 and self.color == 'black':
                promote_pawn(self)
            elif self.y == 840:
                promote_pawn(self)

    def check_possible(self):
        """
        Check and highlight possible moves for the pawn.
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

def promote_pawn(pawn):
    """
    Promote the pawn to a different chess piece.

    Parameters:
    - pawn (Pawn): The pawn to be promoted.
    """
    # Create a dialog window
    dialog = QDialog()
    dialog.setWindowTitle("Choose a piece")
    dialog.setModal(True)

    # Add buttons to choose a piece
    queen_button = QPushButton("Queen")
    queen_button.clicked.connect(lambda: promote_pawn_to(dialog, pawn, "queen"))

    rook_button = QPushButton("Rook")
    rook_button.clicked.connect(lambda: promote_pawn_to(dialog, pawn, "rook"))

    bishop_button = QPushButton("Bishop")
    bishop_button.clicked.connect(lambda: promote_pawn_to(dialog, pawn, "bishop"))

    knight_button = QPushButton("Knight")
    knight_button.clicked.connect(lambda: promote_pawn_to(dialog, pawn, "knight"))

    # Add buttons to the dialog window
    layout = QVBoxLayout()
    layout.addWidget(queen_button)
    layout.addWidget(rook_button)
    layout.addWidget(bishop_button)
    layout.addWidget(knight_button)
    dialog.setLayout(layout)

    # Show the dialog window
    dialog.exec_()

def promote_pawn_to(dialog, pawn, piece_type):
    """
    Promote the pawn to a specific chess piece type.

    Parameters:
    - dialog (QDialog): The dialog window.
    - pawn (Pawn): The pawn to be promoted.
    - piece_type (str): The type of chess piece to promote to.
    """
    if piece_type == "queen":
        pawn.scene().addItem(Queen(pawn.x, pawn.y, pawn.size, pawn.color, bq if pawn.color == 'black' else wq))
    elif piece_type == "rook":
        pawn.scene().addItem(Rook(pawn.x, pawn.y, pawn.size, pawn.color, br if pawn.color == 'black' else wr))
    elif piece_type == "bishop":
        pawn.scene().addItem(Bishop(pawn.x, pawn.y, pawn.size, pawn.color, bb if pawn.color == 'black' else wb))
    elif piece_type == "knight":
        pawn.scene().addItem(Knight(pawn.x, pawn.y, pawn.size, pawn.color, bn if pawn.color == 'black' else wn))

    # Remove the pawn from the scene
    pawn.scene().removeItem(pawn)
    dialog.accept()

def update_board(self):
    """
    Update the board by allowing the player to change the board color.

    Parameters:
    - self: Reference to the current object.
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

    # Connect actions to set_board_color function with predefined parameters
    red_action.triggered.connect(lambda: set_board_color('yellow', 'darkBlue', self))
    blue_action.triggered.connect(lambda: set_board_color('white', 'lightGray', self))
    green_action.triggered.connect(lambda: set_board_color('blue', 'darkBlue', self))
    yellow_action.triggered.connect(lambda: set_board_color('yellow', 'red', self))

    # Show the menu at the cursor position
    cursor_pos = QCursor.pos()
    menu.exec_(self.scene().views()[0].mapToGlobal(cursor_pos))

def set_board_color(color, color2, pawn):
    """
    Set the color of the chessboard.

    Parameters:
    - color (str): The color for squares at odd positions.
    - color2 (str): The color for squares at even positions.
    - pawn: Reference to the current object.
    """
    # Set the new color of the chessboard
    for item in pawn.scene().items():
        if isinstance(item, Square):
            if item.pos == 0:
                item.color = QColor(color)
                item.colorbuff = QColor(color)
            else:
                item.color = QColor(color2)
                item.colorbuff = QColor(color2)
            item.update()