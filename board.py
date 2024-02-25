from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QApplication
from pawns.pawn import Pawn 
from pawns.queen import Queen 
from pawns.rook import Rook 
from pawns.bishop import Bishop 
from pawns.knight import Knight 
from pawns.king import King
from pawns.square import Square
from resource import *



class ChessBoard(QGraphicsScene):
    """
    ChessBoard class represents the main game board.

    Attributes:
    - b_view (int): Board view option.
    - square_size (int): Size of each square on the chessboard.
    - current_turn (str): Current turn ('white' or 'black').
    - checkwhite (bool): True if white king is in check.
    - checkblack (bool): True if black king is in check.
    - kingwpos (list): Position of the white king.
    - kingbpos (list): Position of the black king.
    - buffkingwpos (list): Buffer for white king position.
    - buffkingbpos (list): Buffer for black king position.
    - timer1_id (int): Timer ID for white player turn.
    - timer2_id (int): Timer ID for black player turn.

    Methods:
    - check_white(): Check if the white king is in check.
    - check_black(): Check if the black king is in check.
    - timerEvent(event): Handle timer events for player turns.
    - init_board(): Initialize the chessboard with pieces and squares.
    - update_board(x, y, fig): Update the board after a move.

    """

    def __init__(self):
        """
        Initialize the ChessBoard.

        - Sets up initial game state.
        - Initializes timers for player turns.

        """
        super().__init__()
        self.b_view = 1
        self.square_size = 120
        self.current_turn = 'white'
        self.checkwhite = False
        self.checkblack = False
        self.kingwpos = [3*self.square_size, 0*self.square_size]
        self.kingbpos = [4*self.square_size, 7*self.square_size]
        self.buffkingwpos = [3*self.square_size, 0*self.square_size]
        self.buffkingbpos = [4*self.square_size, 7*self.square_size]
        self.init_board()
        self.timer1_id = self.startTimer(1000)
        self.timer2_id = self.startTimer(1000) 

    def check_white(self):
        """
        Check if the white king is in check.

        Returns:
        - bool: True if white king is in check.

        """
        for item in self.items():
            if not isinstance(item, Square) and item.color == 'black':
                if item.is_valid_move2(self.kingwpos[0],self.kingwpos[1]):
                    self.checkwhite = True
                    print("CHECK White")
                    return True
        self.checkwhite = False
        return False

    def check_black(self):
        """
        Check if the black king is in check.

        Returns:
        - bool: True if black king is in check.

        """
        for item in self.items():
            if not isinstance(item, Square) and item.color == 'white':
                if item.is_valid_move2(self.kingbpos[0],self.kingbpos[1]):
                    self.checkblack = True
                    print("CHECK Black")
                    return True
        self.checkblack = True
        return False
    
    def timerEvent(self, event):
        """
        Handle timer events for player turns.

        Parameters:
        - event (QTimerEvent): Timer event triggering the function.

        """
        if event.timerId() == self.timer1_id:
            self.check_white()
        elif event.timerId() == self.timer2_id:
            self.check_black()
        

                

    def init_board(self):
        """
        Initialize the chessboard with pieces and squares.

        """
        self.colors = [[Qt.white, Qt.lightGray],
                       [Qt.yellow, Qt.darkYellow],
                       [Qt.blue, Qt.darkBlue]]
        for row in range(8):
            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size
                color = self.colors[self.b_view - 1][(row + col) % 2]
                pos = (row + col) % 2
                square = Square(x, y, self.square_size, color, pos)
                self.addItem(square)


        wp = ':/wp.png'; bp=':/bp.png'; wr = ':/wr.png'; br = ':/br.png'; wn = ':/wn.png'; bn = ':/bn.png'; wb = ':/wb.png'; bb = ':/bb.png'; wk = ':/wk.png'; bk = ':/bk.png'; wq = ':/wq.png'; bq = ':/bq.png'


        for p in range(8):
            pawn = Pawn(p*self.square_size, 1*self.square_size, self.square_size, 'white', wp)
            self.addItem(pawn)
        for p in range(8):
            pawn = Pawn(p*self.square_size, 6*self.square_size, self.square_size, 'black', bp)
            self.addItem(pawn)

        rook1w = Rook(0*self.square_size, 0*self.square_size, self.square_size, 'white', wr)
        rook2w = Rook(7*self.square_size, 0*self.square_size, self.square_size, 'white', wr)
        self.addItem(rook1w)
        self.addItem(rook2w)
        rook1b = Rook(0*self.square_size, 7*self.square_size, self.square_size, 'black', br)
        rook2b = Rook(7*self.square_size, 7*self.square_size, self.square_size, 'black', br)
        self.addItem(rook1b)
        self.addItem(rook2b)

        knight1w = Knight(1*self.square_size, 0*self.square_size, self.square_size, 'white', wn)
        knight2w = Knight(6*self.square_size, 0*self.square_size, self.square_size, 'white', wn)
        self.addItem(knight1w)
        self.addItem(knight2w)
        knight1b = Knight(1*self.square_size, 7*self.square_size, self.square_size, 'black', bn)
        knight2b = Knight(6*self.square_size, 7*self.square_size, self.square_size, 'black', bn)
        self.addItem(knight1b)
        self.addItem(knight2b)

        bishop1b = Bishop(2*self.square_size, 0*self.square_size, self.square_size, 'white', wb)
        bishop2b = Bishop(5*self.square_size, 0*self.square_size, self.square_size, 'white', wb)
        self.addItem(bishop1b)
        self.addItem(bishop2b)
        bishop1w = Bishop(2*self.square_size, 7*self.square_size, self.square_size, 'black', bb)
        bishop2w = Bishop(5*self.square_size, 7*self.square_size, self.square_size, 'black', bb)
        self.addItem(bishop1w)
        self.addItem(bishop2w)

        kingw = King(3*self.square_size, 0*self.square_size, self.square_size, 'white', wk)
        queenw = Queen(4*self.square_size, 0*self.square_size, self.square_size, 'white', wq)
        self.addItem(kingw)
        self.addItem(queenw)
        kingb = King(4*self.square_size, 7*self.square_size, self.square_size, 'black', bk)
        queenb = Queen(3*self.square_size, 7*self.square_size, self.square_size, 'black', bq)
        self.addItem(kingb)
        self.addItem(queenb)
        
    def update_board(self, x, y, fig):
        """
        Update the board after a move.

        Parameters:
        - x (int): Target x-coordinate for the move.
        - y (int): Target y-coordinate for the move.
        - fig (str): Name of the chess piece class.

        """
        for item in self.items():
            fig_class = globals()[fig]
            if isinstance(item, fig_class):
                if item.is_valid_move(x, y):
                    item.move(x,y)





if __name__ == '__main__':
    app = QApplication([])
    view = QGraphicsView()
    board = ChessBoard()
    view.setScene(board)
    view.show()
    app.exec_()
