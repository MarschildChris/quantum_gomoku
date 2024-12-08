import numpy as np
import piece


class BoardState:
    def __init__(self, size, values=None, evals=None, color=piece.WHITE):
        if np.all(values != None):
            self.values = np.copy(values)
        else:
            self.values = np.full((size, size), piece.EMPTY)

        self.size = size
        self.color = color
        self.last_move = None
        self.winner = 0

    def value(self, position):
        return self.values[position]

    def is_valid_position(self, position):
        """
        Checks if the position is valid for a move.
        Quantum moves are allowed on EMPTY, QBLACK, and QWHITE positions.
        """
        i, j = position
        return (is_valid_position(self.size, position)
                and self.values[i, j] in [piece.EMPTY, piece.QBLACK, piece.QWHITE])  # Allow EMPTY and quantum pieces

    def legal_moves(self):
        prev_move_idxs = self.values != piece.EMPTY
        area_idxs = expand_area(self.size, prev_move_idxs)
        return np.column_stack(np.where(area_idxs == True))

    def next(self, position):
        next_state = BoardState(size=self.size,
                                values=self.values,
                                color=-self.color)
        next_state[position] = next_state.color
        next_state.last_move = tuple(position)
        return next_state


    def is_terminal(self):
        is_win, color = self.check_five_in_a_row()
        is_full = self.is_full()
        if is_full:
            return True
        return is_win


    def check_five_in_a_row(self):
        pattern = np.full((5,), 1)

        black_win = self.check_pattern(pattern * piece.BLACK)
        white_win = self.check_pattern(pattern * piece.WHITE)

        if black_win:
            self.winner = piece.BLACK
            return True, piece.BLACK
        if white_win:
            self.winner = piece.WHITE
            return True, piece.WHITE
        return False, piece.EMPTY

    def check_three_with_open_ends(self):
        """
        Checks if there is a sequence of 4 same-colored pieces in a row (horizontally,
        vertically, or diagonally) with empty spaces at both ends.

        :return: (True, color) if such a sequence exists, otherwise (False, piece.EMPTY).
        """
        # Define patterns for black and white
        black_pattern = np.array([piece.EMPTY, piece.BLACK, piece.BLACK, piece.BLACK, piece.EMPTY])
        white_pattern = np.array([piece.EMPTY, piece.WHITE, piece.WHITE, piece.WHITE, piece.EMPTY])

        # Check for patterns in all lines
        if self.check_pattern(black_pattern):
            return True, piece.BLACK
        if self.check_pattern(white_pattern):
            return True, piece.WHITE

        return False, piece.EMPTY

    def is_full(self):
        return not np.any(self.values == piece.EMPTY)

    def check_pattern(self, pattern):
        count = 0
        for line in self.get_lines():
            if issub(line, pattern):
                count += 1
        return count

    def get_lines(self):
        l = []

        # rows and cols
        for i in range(self.size):
            l.append(self.values[i, :])
            l.append(self.values[:, i])

        # 2 diags
        for i in range(-self.size + 5, self.size - 4):
            l.append(np.diag(self.values, k=i))
            l.append(np.diag(np.fliplr(self.values), k=i))

        for line in l:
            yield line

    def update_measurement(self, classic_position, empty_position, classic_color):
        """
        Updates the board state after collapsing a pair of quantum pieces.

        :param classic_position: Tuple (i, j) where the classic piece will be placed.
        :param empty_position: Tuple (i, j) where the position will become empty.
        :param classic_color: The color value of the classic piece (e.g., BLACK or WHITE).
        """
        # Set the positions accordingly
        self[empty_position] = 0  # Empty the chosen position
        self[classic_position] = classic_color  # Set the classic piece

    def __getitem__(self, position):
        i, j = position
        return self.values[i, j]

    def __setitem__(self, position, value):
        i, j = position
        self.values[i, j] = value

    def __str__(self):
        out = ' ' * 3
        out += '{}\n'.format(''.join(
            '{}{}'.format((i + 1) % 10, i < 10 and ' ' or "'")
            for i in range(self.size)
        ))

        for i in range(self.size):
            out += '{}{} '.format(i + 1 < 10 and ' ' or '', i + 1)
            for j in range(self.size):
                # Safely fetch the symbol for the current piece
                piece_symbol = piece.symbols.get(self[i, j], '?')
                out += piece_symbol

                # Highlight the last move
                if self.last_move and (i, j) == tuple(self.last_move):
                    out += '*'
                else:
                    out += ' '
            if i != self.size - 1:
                out += '\n'
        return out

    def __repr__(self):
        return self.__str__()


def issub(l, subl):
    l_size = len(l)
    subl_size = len(subl)
    for i in range(l_size - subl_size):
        curr = l[i:min(i + subl_size, l_size - 1)]
        if (curr == subl).all():
            return True
    return False


def expand_area(size, idxs):
    area_idxs = np.copy(idxs)
    for i in range(size):
        for j in range(size):
            if not idxs[i, j]:
                continue
            for direction in ((1, 0), (0, 1), (1, 1), (1, -1)):
                di, dj = direction
                for side in (1, -1):
                    ni = i + di * side
                    nj = j + dj * side
                    if not is_valid_position(size, (ni, nj)):
                        continue
                    area_idxs[ni, nj] = True
    return np.bitwise_xor(area_idxs, idxs)



def is_valid_position(board_size, position):
    i, j = position
    return i >= 0 and i < board_size and j >= 0 and j < board_size
