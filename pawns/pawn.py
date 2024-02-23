from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QBrush, QColor, QPen, QFont, QTransform, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsItem,QDialog, QPushButton, QVBoxLayout, QGraphicsScene, QGraphicsView, QApplication, QMenu, QAction
from pawns.square import Square
from pawns.queen import Queen 
from pawns.rook import Rook 
from pawns.bishop import Bishop 
from pawns.knight import Knight 
from resource import *


wp = ':/wp.png'; bp=':/bp.png'; wr = ':/wr.png'; br = ':/br.png'; wn = ':/wn.png'; bn = ':/bn.png'; wb = ':/wb.png'; bb = ':/bb.png'; wk = ':/wk.png'; bk = ':/bk.png'; wq = ':/wq.png'; bq = ':/bq.png'
      

class Pawn(QGraphicsItem):
    def __init__(self, x, y, size, color, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.setPos(self.x,self.y)
        self.size = size
        self.color = color
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.image = QPixmap(image_path).scaled(self.size, self.size)
        self.first_move = True
        self.buffx = x
        self.buffy = y
        self.removed_item = 0

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget):
        rect = self.boundingRect()
        painter.drawPixmap(rect, self.image , QRectF())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.offset = event.pos() - self.pos()
            self.check_possible()
        if event.button() == Qt.RightButton:
            update_board(self)
    
    def is_valid_move(self, x, y):
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
                    
                if dy == 240 and self.first_move and not self.collides_with_pawns_on_the_way(x,y):
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
                    if dx == 0 and not self.collides_with_pawn(x, y) and not self.collides_with_pawns_on_the_way(x,y):
                        return True
                    
                if abs(dy) == 120 and abs(dx) == 120 and self.collides_with_opponent(x, y):
                    return True

        
        return False
    

    def is_valid_move2(self, x, y):
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
        for item in self.scene().items():
            if not isinstance(item, Square) and item.x == x and item.y == y:
                return True
        return False
    
    def collides_with_opponent(self, x, y):
        for item in self.scene().items():
            if not isinstance(item, Square) and item.color != self.color and item.x == x and item.y == y:
                return True
        return False
    
    def remove_opponent(self, x, y):
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
                            self.setPos(self.buffx,self.buffy)
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
                            self.setPos(self.buffx,self.buffy)
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

    
    def move(self,x,y):
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
                    self.setPos(self.buffx,self.buffy)
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
                    self.setPos(self.buffx,self.buffy)
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
        for item in self.scene().items():
            if isinstance(item, Square) and self.is_valid_move(item.x, item.y):
                item.color = QColor(102, 255, 102)
                item.update()

    def uncheck_possible(self):
        for item in self.scene().items():
            if isinstance(item, Square) and self.is_valid_move(item.x, item.y):
                item.color = item.colorbuff
                item.update()






def promote_pawn(pawn):
    # Utwórz okno dialogowe
    dialog = QDialog()
    dialog.setWindowTitle("Wybierz figury")
    dialog.setModal(True)

    # Dodaj przyciski do wyboru figury
    queen_button = QPushButton("Hetman")
    queen_button.clicked.connect(lambda: promote_pawn_to(dialog, pawn, "hetman"))

    rook_button = QPushButton("Wieża")
    rook_button.clicked.connect(lambda: promote_pawn_to(dialog, pawn, "wieza"))

    bishop_button = QPushButton("Goniec")
    bishop_button.clicked.connect(lambda: promote_pawn_to(dialog, pawn, "goniec"))

    knight_button = QPushButton("Skoczek")
    knight_button.clicked.connect(lambda: promote_pawn_to(dialog, pawn, "skoczek"))

    # Dodaj przyciski do okna dialogowego
    layout = QVBoxLayout()
    layout.addWidget(queen_button)
    layout.addWidget(rook_button)
    layout.addWidget(bishop_button)
    layout.addWidget(knight_button)
    dialog.setLayout(layout)

    # Wyświetl okno dialogowe
    dialog.exec_()

def promote_pawn_to(dialog, pawn, piece_type):
    if piece_type == "hetman":
        pawn.scene().addItem(Queen(pawn.x, pawn.y, pawn.size, pawn.color, bq if pawn.color == 'black' else wq))
    elif piece_type == "wieza":
        pawn.scene().addItem(Rook(pawn.x, pawn.y, pawn.size, pawn.color, br if pawn.color == 'black' else wr))
    elif piece_type == "goniec":
        pawn.scene().addItem(Bishop(pawn.x, pawn.y, pawn.size, pawn.color, bb if pawn.color == 'black' else wb))
    elif piece_type == "skoczek":
        pawn.scene().addItem(Knight(pawn.x, pawn.y, pawn.size, pawn.color, bn if pawn.color == 'black' else wn))

    # Zamknij okno dialogowe, jeśli zostało utworzone

    pawn.scene().removeItem(pawn)
    dialog.accept()


def update_board(self):
    menu = QMenu(self.scene().views()[0])
    red_action = QAction('Yellow -  Dark Blue', self.scene().views()[0])
    blue_action = QAction('White - Light Gray', self.scene().views()[0])
    green_action = QAction('Blue - Dark Blue', self.scene().views()[0])
    yellow_action = QAction('Yellow - Red', self.scene().views()[0])
    menu.addAction(red_action)
    menu.addAction(blue_action)
    menu.addAction(green_action)
    menu.addAction(yellow_action)
    # po wybraniu akcji ustawiamy nowy kolor planszy
    red_action.triggered.connect(lambda: set_board_color('yellow','darkBlue', self))
    blue_action.triggered.connect(lambda: set_board_color('white','lightGray', self))
    green_action.triggered.connect(lambda: set_board_color('blue','darkBlue', self))
    yellow_action.triggered.connect(lambda: set_board_color('yellow','red', self))

    # pokazujemy menu w pozycji kursora
    cursor_pos = QCursor.pos()
    menu.exec_(self.scene().views()[0].mapToGlobal(cursor_pos))

def set_board_color(color,color2, pawn):
    # ustawiamy nowy kolor planszy
    for item in pawn.scene().items():
            if isinstance(item, Square):
                if item.pos == 0 :
                    item.color = QColor(color)
                    item.colorbuff = QColor(color)
                else :
                    item.color = QColor(color2)
                    item.colorbuff = QColor(color2)
                item.update()
