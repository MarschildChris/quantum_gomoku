from tkinter import *
import numpy as np
from game import GameRunner  # Import the GameRunner class
from piece import BLACK, WHITE, EMPTY, QBLACK, QWHITE, QBW
import qiskit as qs

# Setup window
myInterface = Tk()
s = Canvas(myInterface, width=800, height=800, background="#e8e0c8")
s.pack()

# Board size and spacing
Board_Size = 15
Frame_Gap = 35
width = 500
height = 500

# Grid settings
Board_X1 = width / 10
Board_Y1 = height / 10
Board_GapX = (width - Board_X1 * 2) / Board_Size
Board_GapY = (height - Board_Y1 * 2) / Board_Size
Chess_Radius = (Board_GapX * (9 / 10)) / 2

# Game state variables
Turn_Num = 1
Turn = "black"  # Start with black piece
Winner = None
board = [[0] * (Board_Size + 1) for _ in range(Board_Size + 1)]  # Initialize the board (0 = empty)
# Initialize GameRunner for AI
ai_game = GameRunner(size=Board_Size)
color=-1 ##important

# Create board grid
def draw_grid():
    s.create_rectangle(Board_X1 - Frame_Gap, Board_Y1 - Frame_Gap,
                       Board_X1 + Frame_Gap + Board_GapX * (Board_Size-1), Board_Y1 + Frame_Gap + Board_GapY * (Board_Size-1), width=3)

    for f in range(Board_Size):
        s.create_line(Board_X1, Board_Y1 + f * Board_GapY, Board_X1 + Board_GapX * (Board_Size-1), Board_Y1 + f * Board_GapY)
        s.create_line(Board_X1 + f * Board_GapX, Board_Y1, Board_X1 + f * Board_GapX, Board_Y1 + Board_GapY * (Board_Size-1))

        s.create_text(Board_X1 - Frame_Gap * 1.7, Board_Y1 + f * Board_GapY, text=f + 1, font="Helvetica 10 bold", fill="black")
        s.create_text(Board_X1 + f * Board_GapX, Board_Y1 - Frame_Gap * 1.7, text=f + 1, font="Helvetica 10 bold", fill="black")

draw_grid()

# Quantum move state
is_quantum_mode = False
quantum_moves = []  # Track the two moves for the quantum piece
quantum_pieces = []  # Track all quantum pieces for potential collapse
black_quantum_pieces = []
white_quantum_pieces = []

# Global variable to track measurement state
is_measure_mode = False

def create_circuit():
    """
    Creates a quantum circuit for the Bell state 1/sqrt(2) (|01> + |10>).

    Returns:
        QuantumCircuit: The quantum circuit generating the desired Bell state.
    """
    # Create a quantum circuit with 2 qubits
    qc = qs.QuantumCircuit(2)

    # Initialize qubit 0 to |1> (apply an X gate)
    qc.x(0)

    # Apply a Hadamard gate to qubit 0
    qc.h(1)

    # Apply a CNOT gate with qubit 0 as control and qubit 1 as target
    qc.cx(0, 1)

    return qc


# Show the Cancel button
def show_cancel_button():
    cancel_button.place(x=width / 2 * 0.5 + 220, y=height + Frame_Gap-50, height=Chess_Radius * 2, width=Chess_Radius * 7)

# Hide the Cancel button
def hide_cancel_button():
    cancel_button.place_forget()


def handle_quantum_move():
    global is_quantum_mode, quantum_moves, is_measure_mode
    is_measure_mode = False
    if not Winner:  # Allow quantum move only if the game is not over
        is_quantum_mode = True
        quantum_moves = []
        show_cancel_button()  # Show the Cancel button
        print("Quantum mode activated! Place two pieces.")

def handle_measure():
    global is_measure_mode, is_quantum_mode
    is_quantum_mode = False
    if not Winner:  # Allow measurement only if the game is not over
        is_measure_mode = True
        show_cancel_button()  # Show the Cancel button
        print("Measurement mode activated! Click on a quantum piece to collapse.")

def handle_cancel():
    global is_quantum_mode, is_measure_mode
    is_quantum_mode = False
    is_measure_mode = False
    hide_cancel_button()  # Hide the Cancel button
    print("Returned to normal mode.")




# Modified MouseClick function to handle measurement
def MouseClick(event):
    global Turn_Num, Turn, Winner, is_quantum_mode, is_measure_mode, quantum_moves
    X_click = event.x
    Y_click = event.y

    # Find grid position based on click coordinates
    X = int((X_click - Board_X1 + Board_GapX / 2) / Board_GapX)
    Y = int((Y_click - Board_Y1 + Board_GapY / 2) / Board_GapY)

    # Make sure the click is within bounds
    if X < 0 or X >= Board_Size or Y < 0 or Y >= Board_Size:
        return

    if Winner != None:
        return

    print("white quantum pieces:", white_quantum_pieces)
    print("black quantum pieces:", black_quantum_pieces)

    if is_measure_mode:
        # Check if clicked spot is a quantum piece
        print((Y,X),"Y,X")
        print(quantum_pieces)
        if (Y, X) in quantum_pieces:
            print("black quantum pieces before", black_quantum_pieces)
            print("white quantum pieces before", white_quantum_pieces)
            collapse_quantum_piece(Y, X)
            is_measure_mode = False  # Exit measure mode after collapsing a piece
            hide_cancel_button()  # Automatically hide the Cancel button
            if check_winner():
                Winner = Turn
                s.create_text(width / 2, height / 2, text=f"{Turn.upper()} WINS!", font="Helvetica 20 bold", fill="red")
                return

        else:
            print("No quantum piece selected. Try again.")
        return


    # Handle quantum move mode
    if is_quantum_mode:
        if (Y, X) in quantum_pieces:  # Check if the spot is already occupied by a quantum piece
            current_piece = board[Y][X]
            if (current_piece == 2 and Turn == "white") or (current_piece == -2 and Turn == "black"):
                # Overlap between opposite colors
                delete_piece(X, Y)  # Remove the existing quantum piece's visual representation
                create_quantum_piece(X, Y, "grey")  # Create a grey quantum piece visually
                board[Y][X] = 3  # Mark as grey quantum piece (QBW) on the board
                print(f"Grey quantum piece formed at ({X}, {Y}) due to overlap.")
                quantum_moves.append((Y, X))  # Count this as one of the quantum moves
                if current_piece == 2:
                    white_quantum_pieces.append((Y, X))
                else:
                    black_quantum_pieces.append((Y, X))
            elif current_piece in [2, -2]:
                print("Cannot overlap two pieces of the same color.")
                return
            elif current_piece == 3:  # Already a grey quantum piece
                print("Cannot place on a grey quantum piece.")
                return
        elif board[Y][X] == 0:  # Place a new quantum piece if the spot is empty
            color = "black" if Turn == "black" else "white"
            create_quantum_piece(X, Y, color)
            quantum_moves.append((Y, X))
            board[Y][X] = 2 if Turn == "black" else -2  # Temporarily mark the spot
            print(f"Quantum piece placed at ({X}, {Y})")
            quantum_pieces.append((Y, X))
            if Turn == "white":
                white_quantum_pieces.append((Y, X))
            else:
                black_quantum_pieces.append((Y, X))

        if len(quantum_moves) == 2:  # When two moves are made
            print("Quantum move completed!")
            ai_game.play_quantum(quantum_moves)  # Pass moves to the game logic
            is_quantum_mode = False
            quantum_moves = []
            hide_cancel_button()  # Automatically hide the Cancel button

            # Ensure the AI plays immediately after the quantum move
            Turn = "white" if Turn == "black" else "black"
            Turn_Num += 1
            ai_turn()
        return


    else:
        # Handle normal move
        if board[Y][X] == 0:
            color = "black" if Turn == "black" else "white"
            create_piece(X, Y, color)

            # Update the board state
            board[Y][X] = 1 if Turn == "black" else 2
            ai_game.play(Y, X)  # Update the GameRunner state with the player's move

            # Check for winner
            if check_winner():
                Winner = Turn
                s.create_text(width / 2, height / 2, text=f"{Turn.upper()} WINS!", font="Helvetica 20 bold", fill="red")
                return

            # Switch turns
            Turn = "white" if Turn == "black" else "black"
            Turn_Num += 1

            # Let the AI play its turn
            ai_turn()


# Dictionary to store piece references by their location
pieces = {}  # Key: (x, y), Value: ID of the created canvas item


# Draw the piece on the board
def create_piece(x, y, color):
    global pieces
    radius = Chess_Radius
    fill = color

    # Create the oval representing the piece
    piece_id = s.create_oval(Board_X1 + x * Board_GapX - radius,
                             Board_Y1 + y * Board_GapY - radius,
                             Board_X1 + x * Board_GapX + radius,
                             Board_Y1 + y * Board_GapY + radius,
                             fill=fill, outline="black", width=2)

    # Store the piece ID in the dictionary
    pieces[(x, y)] = piece_id


# Delete the piece at the specified location
def delete_piece(x, y):
    global pieces

    # Check if there is a piece at the given location
    if (x, y) in pieces:
        # Delete the canvas item
        s.delete(pieces[(x, y)])
        # Remove the piece reference from the dictionary
        del pieces[(x, y)]
    else:
        print(f"No piece found at ({x}, {y}) to delete.")




def create_quantum_piece(x, y, color):
    global pieces, quantum_pieces
    radius = Chess_Radius

    # Define fill and outline colors based on the piece color
    if color == "grey":
        outline = "#808080"  # Grey outline to match the piece
    else:
        outline = color

    # Create the visual representation of the quantum piece
    piece_id = s.create_oval(Board_X1 + x * Board_GapX - radius,
                             Board_Y1 + y * Board_GapY - radius,
                             Board_X1 + x * Board_GapX + radius,
                             Board_Y1 + y * Board_GapY + radius,
                             outline=outline, width=2)

    # Add the piece ID to the dictionary for tracking
    pieces[(x, y)] = piece_id



# Let the AI make its move
def ai_turn():
    global Turn_Num, Turn, Winner, white_quantum_pieces
    ai_played, move = ai_game.aiplay()
    if ai_played:
        if isinstance(move, list) and len(move) == 2:  # Check if AI played a quantum move
            color = "black" if Turn == "black" else "white"
            for Y, X in move:  # Iterate over the two quantum positions
                create_quantum_piece(X, Y, color)
                board[Y][X] = 2 if Turn == "black" else -2  # Update board with quantum piece marker
                quantum_pieces.append((Y, X))  # Track quantum pieces for potential collapse
                white_quantum_pieces.append((Y, X))
            print(f"AI placed quantum pieces at {move[0]} and {move[1]}")
        else:
            Y, X = move  # Normal move
            color = "black" if Turn == "black" else "white"
            create_piece(X, Y, color)
            board[Y][X] = 1 if Turn == "black" else -1  # Update board with classic piece
            print(f"AI played at {move}")

        # Check for winner
        if check_winner():
            Winner = Turn
            s.create_text(width / 2, height / 2, text=f"{Turn.upper()} WINS!", font="Helvetica 20 bold", fill="red")
            return

        # Switch turns
    Turn = "white" if Turn == "black" else "black"
    Turn_Num += 1


def check_winner():
    """
    Uses the GameRunner's get_status method to determine if there is a winner.

    :param x: x-coordinate of the last move.
    :param y: y-coordinate of the last move.
    :return: True if a winner exists or the game is a draw, otherwise False.
    """
    global Winner

    # Fetch the current game status
    status = ai_game.get_status()

    # Check if the game is finished and assign the winner if applicable
    if status['finished']:
        winner = status['winner']
        if winner == BLACK:
            Winner = "black"
        elif winner == WHITE:
            Winner = "white"
        else:
            Winner = "draw"
        return True

    return False


# Restart the game
def restart_game():
    global Turn_Num, Turn, Winner, board, ai_game, pieces, quantum_pieces, white_quantum_pieces, black_quantum_pieces
    Turn_Num = 1
    Turn = "black"
    Winner = None
    board = [[0] * (Board_Size + 1) for _ in range(Board_Size + 1)]  # Reset the board
    ai_game.restart()  # Reset the AI game state
    pieces = {}
    quantum_pieces=[]
    white_quantum_pieces=[]
    black_quantum_pieces=[]

    # Clear the board canvas
    s.delete("all")
    draw_grid()  # Redraw the grid

# Create the Restart button
restart_button = Button(myInterface, text="Restart", font="Helvetica 14", command=restart_game)
restart_button.place(x=width / 2 * 0.5 - 80, y=height + Frame_Gap-50, height=Chess_Radius * 2, width=Chess_Radius * 7)

quantum_button = Button(myInterface, text="Quantum", font="Helvetica 14", command=handle_quantum_move)
quantum_button.place(x=width / 2 * 0.5 + 20, y=height + Frame_Gap-50, height=Chess_Radius * 2, width=Chess_Radius * 7)

def print_board_state():
    print("\nBoard State:")
    for y in range(Board_Size):
        row = []
        for x in range(Board_Size):
            piece = board[y][x]
            if piece == 0:
                row.append(".")  # Empty space
            elif piece == 1:
                row.append("X")  # Black classic piece
            elif piece == 2:
                row.append("B")  # Black quantum piece
            elif piece == -1:
                row.append("O")  # White classic piece
            elif piece == -2:
                row.append("W")  # White quantum piece
            elif piece == 3:
                row.append("Q")  # Grey quantum piece
            else:
                row.append("?")  # Unknown state (for safety)
        print(" ".join(row))
    print("\n")


import random  # Import random for random selection
def collapse_quantum_piece(y, x, is_determined=False, advance_turn=True):
    """
    Collapses quantum pieces into classical pieces or clears them based on a determined or random outcome.
    """
    global board, white_quantum_pieces, black_quantum_pieces, Turn, Turn_Num, Winner

    # Identify the quantum piece color and list
    if board[y][x] == QBLACK or (y, x) in black_quantum_pieces:
        quantum_list = black_quantum_pieces
        piece_color = "black"
        classic_color = BLACK
    elif board[y][x] == QWHITE or (y, x) in white_quantum_pieces:
        quantum_list = white_quantum_pieces
        piece_color = "white"
        classic_color = WHITE
    else:
        print(f"No quantum piece to collapse at ({y}, {x}).")
        return

    # Locate the pair of the quantum piece
    if (y, x) in quantum_list:
        index = quantum_list.index((y, x))
        if index % 2 != 0:
            p_index = index-1
        else:
            p_index = index +1
    else:
        print(f"Quantum piece at ({y}, {x}) not found in quantum list.")
        return

    pos1 = quantum_list[index]
    pos2 = quantum_list[p_index]

    # Determine collapse outcome
    collapse_to_pos1 = 1 if is_determined else np.random.choice([0, 1])
    if collapse_to_pos1:
        classic_pos, empty_pos = pos1, pos2
    else:
        classic_pos, empty_pos = pos2, pos1

    # Remove visual representations of both quantum pieces
    delete_piece(pos1[1], pos1[0])
    delete_piece(pos2[1], pos2[0])

    # Create the classic piece at the collapsed position
    create_piece(classic_pos[1], classic_pos[0], piece_color)
    board[classic_pos[0]][classic_pos[1]] = classic_color

    # Clear the empty position
    board[empty_pos[0]][empty_pos[1]] = EMPTY

    # Remove the pair from the quantum list
    quantum_list.remove(pos1)
    quantum_list.remove(pos2)

    # Check for secondary collapses
    if classic_pos in black_quantum_pieces or classic_pos in white_quantum_pieces:
        collapse_quantum_piece(classic_pos[0], classic_pos[1], is_determined=True, advance_turn=False)

    # Notify game logic
    ai_game.measure_quantum(classic_pos, empty_pos, classic_color)

    print(f"Collapsed quantum piece at {classic_pos}, cleared {empty_pos}.")

    # Advance turn if needed
    if advance_turn:
        Turn = "white" if Turn == "black" else "black"
        print_board_state()
        if check_winner():
            Winner = Turn
            s.create_text(width / 2, height / 2, text=f"{Turn.upper()} WINS!", font="Helvetica 20 bold", fill="red")
            return
        Turn_Num += 1
        ai_turn()






# Create the Measure button
measure_button = Button(myInterface, text="Measure", font="Helvetica 14", command=handle_measure)
measure_button.place(x=width / 2 * 0.5 + 120, y=height + Frame_Gap-50, height=Chess_Radius * 2, width=Chess_Radius * 7)

# Create the Cancel button (initially hidden)
cancel_button = Button(myInterface, text="Cancel", font="Helvetica 14", command=handle_cancel)
cancel_button.place_forget()  # Hide the button initially


# Bind the click event to the canvas
s.bind("<Button-1>", MouseClick)

# Run the game
myInterface.mainloop()
