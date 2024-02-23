#Implementation chess game in Python

The project is launched by running the main.py file. The main window is displayed, to which a board is attached as a scene, two clocks as widgets, and a text field as a text line.

Chess pieces implement the following commands:
Inheritance from QGraphicsScene (chessboard located in the board.py file).
Inheritance from QGraphicsItem (pawn classes in the pawns folder).
Each piece is clickable and draggable. Clicking, dragging, and dropping a piece implements its move. Right-clicking on any piece displays a menu allowing you to change the board's color.
In the top-left corner of the screen, there is a text field allowing movement of pieces using chess notation. Chess notation is in the form Nxy, where N is the type of piece in Polish chess notation ('K' - 'King'; 'H' - 'Queen'; 'S' - 'Knight'; 'G' - 'Bishop'; 'W' - 'Rook'; none - 'Pawn'), x - column, y - row.
Graphics are imported from the resources.qrc file.
Holding a piece highlights possible moves.
The game implements some rules (turn-based play, capturing pieces, pawn promotion, checking for check).
There are two clickable analog clocks on the screen counting down from 5 minutes. Clicking any clock stops the clicked clock. The clocks have not yet been connected to the rest of the game.
Used libraries: PyQt5, resources, sys.
