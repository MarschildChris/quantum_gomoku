import numpy as np
from board import BoardState
from ai import get_best_move
from piece import BLACK, WHITE, EMPTY, QBLACK, QWHITE, QBW  # Import quantum pieces


class GameRunner:
    def __init__(self, size=19, depth=2):
        self.size = size
        self.depth = depth
        self.finished = False
        self.restart()

    def print_board(self):
        print(self.state)

    def restart(self, player_index=1):
        self.is_max_state = True if player_index == -1 else False
        self.state = BoardState(self.size)
        self.ai_color = -player_index

    def play(self, i, j):
        position = (i, j)
        if self.state.color != self.ai_color:
            return False
        if not self.state.is_valid_position(position):
            return False
        self.state = self.state.next(position)
        self.finished = self.state.is_terminal()
        print("user played!")
        self.print_board()
        return True

    def play_quantum(self, moves):
        """
        Handles the placement of quantum pieces, including overlaps.
        """
        if len(moves) != 2:
            print("Quantum move requires exactly two positions.")
            return False

        quantum_piece = QBLACK if self.state.color == WHITE else QWHITE

        for i, j in moves:
            # Check the current state of the position
            current_piece = self.state.values[i][j]

            if current_piece == EMPTY:  # Place a new quantum piece
                self.state.values[i][j] = quantum_piece
            elif current_piece in [QBLACK, QWHITE]:  # Handle overlap between opposite quantum pieces
                if current_piece != quantum_piece:  # Overlap between black and white
                    self.state.values[i][j] = QBW  # Convert to grey quantum piece
                else:  # Same-color overlap is invalid
                    print(
                        f"Invalid move: Cannot overlap two {('black' if quantum_piece == QBLACK else 'white')} quantum pieces.")
                    return False
            elif current_piece == QBW:  # Grey pieces cannot be overlapped
                print(f"Invalid move at position ({i}, {j}): Cannot overlap grey quantum pieces.")
                return False
            else:  # Invalid move
                print(f"Invalid quantum move at position ({i}, {j}).")
                return False

        # Change turn after the quantum move
        self.state.color = -self.state.color
        print(f"Quantum move placed at {moves}, including overlaps.")
        self.finished = self.state.is_terminal()  # Check if the game ends with this move
        self.print_board()

        return True

    def measure_quantum(self, classic_position, empty_position, classic_color):
        """
        Updates the board state after collapsing a pair of quantum pieces.

        :param classic_position: Tuple (i, j) where the classic piece will be placed.
        :param empty_position: Tuple (i, j) where the position will become empty.
        :param classic_color: The color value of the classic piece (e.g., BLACK or WHITE).
        """
        # Update the board state
        self.state.update_measurement(classic_position, empty_position, classic_color)

        # Change turn after the measurement
        self.state.color = -self.state.color

        print(f"Measurement updated: classic at {classic_position}, empty at {empty_position}")
        self.print_board()

    def aiplay(self):
        if self.state.color == self.ai_color:
            return False, (0, 0)

        if self.state is None:
            print("Error: Game state is not initialized.")
            return False, None  # Safely return in case of uninitialized state

        # Call the check_three_with_open_ends method
        is_three_with_open_ends, color = self.state.check_three_with_open_ends()


        if is_three_with_open_ends and color==1:
            print("ai playing quantum!")
            # AI places two quantum pieces
            first_move, _ = get_best_move(self.state, self.depth, self.is_max_state)
            # Simulate the first move to calculate the second move
            temp_state = self.state.next(first_move)
            second_move, _ = get_best_move(temp_state, self.depth, self.is_max_state)

            # Place the quantum pieces
            self.play_quantum([first_move, second_move])
            print(f"AI placed quantum pieces at {first_move} and {second_move}.")
            return True, [first_move, second_move]


        move, value = get_best_move(self.state, self.depth, self.is_max_state)
        self.state = self.state.next(move)
        self.finished = self.state.is_terminal()
        print("ai played!")
        self.print_board()
        return True, move

    def get_status(self):
        board = self.state.values
        return {
            'board': board.tolist(),
            'next': -self.state.color,
            'finished': self.finished,
            'winner': self.state.winner,
        }
