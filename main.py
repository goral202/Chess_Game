import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QDockWidget, QLineEdit
from PyQt5.QtCore import Qt
from board import ChessBoard
from clocks import Clock

class Window(QMainWindow):
    """
    Window class represents the main application window for the chess game.

    Attributes:
    - scene (ChessBoard): Chess board scene for the game.
    - view (QGraphicsView): Graphics view displaying the chess board.
    - chess_dock_widget, clock1_dock_widget, clock2_dock_widget (QDockWidget): Dock widgets for chess board and two clocks.
    - text_field (QLineEdit): Text field for entering chess moves.

    Methods:
    - __init__(): Initialize the main window and set up widgets.
    - handle_notation_move(): Handle chess move input in algebraic notation.
    - convert_notation_to_coord(notation): Convert algebraic notation to board coordinates.

    """

    def __init__(self):
        """
        Initialize the main window.

        - Set up chess board, dock widgets for the chess board and clocks, and a text field for move input.

        """
        super().__init__()

        # Chess board setup
        self.scene = ChessBoard()
        self.view = QGraphicsView(self.scene, self)

        # Dock widget for chess board
        self.chess_dock_widget = QDockWidget(self)
        self.chess_dock_widget.setWidget(self.view)
        self.chess_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)

        # Dock widget for clock 1
        self.clock1_dock_widget = QDockWidget(self)
        self.clock1_dock_widget.setWidget(Clock())
        self.clock1_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.clock1_dock_widget)

        # Dock widget for clock 2
        self.clock2_dock_widget = QDockWidget(self)
        self.clock2_dock_widget.setWidget(Clock())
        self.clock2_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.clock2_dock_widget)

        # Set positions and sizes for dock widgets
        self.chess_dock_widget.setFloating(False)
        self.chess_dock_widget.setGeometry(0, 0, 800, 600)
        self.clock1_dock_widget.setFloating(False)
        self.clock1_dock_widget.setGeometry(800, 0, 100, 200)
        self.clock2_dock_widget.setFloating(False)
        self.clock2_dock_widget.setGeometry(800, 300, 100, 200)

        # Create a text field for move input
        self.text_field = QLineEdit(self)
        self.text_field.setGeometry(20, 20, 200, 30)
        self.text_field.returnPressed.connect(self.handle_notation_move)

        # Set central widget and dock widgets
        self.setCentralWidget(self.chess_dock_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.chess_dock_widget)

        # Set window properties
        self.setWindowTitle("Chess")
        self.setMinimumSize(1200, 600)
        self.show()

    def handle_notation_move(self):
        """
        Handle chess move input in algebraic notation.

        - Parse the input notation and update the chess board.

        """
        notation = self.text_field.text()
        x, y, fig = self.convert_notation_to_coord(notation)
        self.scene.update_board(x, y, fig)

    def convert_notation_to_coord(self, notation):
        """
        Convert algebraic notation to board coordinates.

        Parameters:
        - notation (str): Algebraic chess move notation (e.g., 'd4').

        Returns:
        - Tuple (int, int, str): X-coordinate, Y-coordinate, and chess piece type.

        """
        # Check if notation has the correct length
        if len(notation) < 2:
            raise ValueError("Invalid chess notation")

        # Get character values from notation
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
            else:
                raise ValueError("Invalid chess notation")
        else:
            fig = 'Pawn'

        # Check if values are within range
        if letter < 'a' or letter > 'h' or number < 1 or number > 8:
            raise ValueError("Invalid chess notation")

        # Convert values to coordinates
        x = ord(letter) - ord('a')
        y = 8 - number
        return x * 120, y * 120, fig

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())  # Start the main event loop