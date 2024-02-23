from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtGui import QColor, QTransform, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QMenu, QAction
from pawns.square import Square



class Bishop(QGraphicsItem):
    def __init__(self, x, y, size, color, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.setPos(self.x,self.y)
        self.size = size
        self.color = color
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.image = QPixmap(image_path).scaled(self.size, self.size)
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
                
                if (abs(dy)/120) == (abs(dx)/120) :
                    if not self.collides_with_pawns_on_the_way(x, y) and self.collides_with_opponent(x,y):
                        return True
        if self.scene().current_turn == 'black':             
            if self.color == 'black':

                if (abs(dy)/120) == (abs(dx)/120) :
                    if not self.collides_with_pawns_on_the_way(x, y) and self.collides_with_opponent(x,y):
                        return True
        return False
    
    def is_valid_move2(self, x, y):
        if x < 0 or x > 960 or y < 0 or y > 960:
            return False
        
        dx = x - self.x
        dy = y - self.y
        if self.color == 'white':
            
            if (abs(dy)/120) == (abs(dx)/120) :
                if not self.collides_with_pawns_on_the_way(x, y) and self.collides_with_opponent(x,y):
                    return True          
        if self.color == 'black':

            if (abs(dy)/120) == (abs(dx)/120) :
                if not self.collides_with_pawns_on_the_way(x, y) and self.collides_with_opponent(x,y):
                    return True
        return False

    def collides_with_pawn(self, x, y):
        for item in self.scene().items():
            if not isinstance(item, Square) and item.x == x and item.y == y and item.color != self.color:
                return True
        return False
    
    def collides_with_opponent(self, x, y):
        for item in self.scene().items():
            if not isinstance(item, Square) and item.color != self.color and item.x == x and item.y == y:
                return True
            if not isinstance(item, Square) and item.color == self.color and item.x == x and item.y == y:
                return False
        return True
    
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
        dx = x - self.x
        dy = y - self.y
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1
        xt, yt = self.x + sx * 120, self.y + sy * 120
        i = 0
        while x != xt and y != yt:
            for item in self.scene().items():
                i+=1
                if not isinstance(item, Square) and item.x == xt and item.y == yt:
                    return True
            xt += sx * 120
            yt += sy * 120
            if(i > 256):
                break
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
                    if self.scene().current_turn == 'white':
                        self.scene().current_turn = 'black'
                    else:
                        self.scene().current_turn = 'white'

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

    # def mouseMoveEvent(self, event):
    #     super().mouseMoveEvent(event)
    #     if event.buttons() & Qt.LeftButton:
    #         self.setPos(event.pos() - self.offset)


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
    red_action.triggered.connect(lambda: set_board_color('yellow','darkBlue', self))
    blue_action.triggered.connect(lambda: set_board_color('white','lightGray', self))
    green_action.triggered.connect(lambda: set_board_color('blue','darkBlue', self))
    yellow_action.triggered.connect(lambda: set_board_color('yellow','red', self))
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