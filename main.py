import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QDockWidget, QLineEdit
from PyQt5.QtCore import Qt
from board import ChessBoard
from clocks import Clock


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # szachownica
        self.scene = ChessBoard()
        self.view = QGraphicsView(self.scene, self)

        # dock widget dla szachownicy
        self.chess_dock_widget = QDockWidget(self)
        self.chess_dock_widget.setWidget(self.view)
        self.chess_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)

        # dock widget dla zegara 1
        self.clock1_dock_widget = QDockWidget(self)
        self.clock1_dock_widget.setWidget(Clock())
        self.clock1_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.clock1_dock_widget)

        # dock widget dla zegara 2
        self.clock2_dock_widget = QDockWidget(self)
        self.clock2_dock_widget.setWidget(Clock())
        self.clock2_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.clock2_dock_widget)

        # ustawienia położenia i rozmiaru dock widget-ów
        self.chess_dock_widget.setFloating(False)
        self.chess_dock_widget.setGeometry(0, 0, 800, 600)
        self.clock1_dock_widget.setFloating(False)
        self.clock1_dock_widget.setGeometry(800, 0, 100, 200)
        self.clock2_dock_widget.setFloating(False)
        self.clock2_dock_widget.setGeometry(800, 300, 100, 200)

        # utworzenie pola tekstowego
        self.text_field = QLineEdit(self)
        self.text_field.setGeometry(20, 20, 200, 30)
        self.text_field.returnPressed.connect(self.handle_notation_move)

        # ustawienie centralnego widżetu i dock widget-ów
        self.setCentralWidget(self.chess_dock_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.chess_dock_widget)

        self.setWindowTitle("Chess")
        self.setMinimumSize(1200, 600)
        self.show()

    def handle_notation_move(self):
        notation = self.text_field.text()
        x,y,fig = convert_notation_to_coord(notation)
        self.scene.update_board(x, y, fig)

def convert_notation_to_coord(notation):
    """
    Konwertuje notację szachową (np. 'd4') na koordynaty na planszy (np. (3, 3))
    """
    # Sprawdzamy, czy notacja ma odpowiednią długość
    if len(notation) < 2:
        raise ValueError("Nieprawidłowa notacja szachowa")

    # Pobieramy wartości znaków z notacji
    letter = notation[-2].lower()
    number = int(notation[-1])
    figura = notation[:-2]

    if len(figura):
        fig = figura[0]
        if fig == 'K':
            fig = 'King'
        elif fig == 'H':
            fig = 'Queen'
        elif fig == 'S':
            fig = 'Knight'
        elif fig == 'G':
            fig = 'Bishop'
        elif fig == 'W':
            fig = 'Rook'
        else: raise ValueError("Nieprawidłowa notacja szachowa")
    else: fig = 'Pawn'


    # Sprawdzamy, czy wartości są w zakresie
    if letter < 'a' or letter > 'h' or number < 1 or number > 8:
        raise ValueError("Nieprawidłowa notacja szachowa")

    # Przeliczamy wartości na koordynaty
    x = ord(letter) - ord('a')
    y = 8 - number
    return x*120, y*120, fig

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())  # Start main event loop
