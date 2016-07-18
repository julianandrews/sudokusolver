class BacktrackingSolver:
    def solve(self, state):
        if self.is_a_solution(state):
            return state

        for move in self.get_candidate_moves(state):
            self.make_move(move, state)
            solution = self.solve(state)
            if solution:
                return solution
            else:
                self.unmake_move(move, state)

        return None

    def is_a_solution(self, state):
        raise NotImplemented

    def get_candidate_moves(self, state):
        raise NotImplemented

    def make_move(self, move, state):
        raise NotImplemented

    def unmake_move(self, move, state):
        raise NotImplemented


class BacktrackingSudokuSolver(BacktrackingSolver):
    def is_a_solution(self, board):
        return board.full

    def get_candidate_moves(self, board):
        candidate_squares = board.empty_squares
        possible_moves = [board.moves_for_square(x, y) for (x, y) in candidate_squares]
        i, values = min(enumerate(possible_moves), key=lambda args: len(args[1]))
        x, y = candidate_squares[i]
        return [(x, y, value) for value in values]

    def make_move(self, move, board):
        x, y, value = move
        board.set_value(x, y, value)

    def unmake_move(self, move, board):
        x, y, value = move
        board.set_value(x, y, None)


class SudokuBoard:
    def __init__(self, board):
        self.exclusion_counts = [[[0] * 9 for i in range(9)] for j in range(9)]

        self.board = [[None] * 9 for j in range(9)]
        for y, row in enumerate(board):
            for x, value in enumerate(row):
                if value is not None:
                    self.set_value(x, y, value)

    def set_value(self, x, y, value):
        excluded_index = (value if value is not None else self.board[y][x]) - 1
        increment = 1 if value is not None else -1
        for i in range(9):
            self.exclusion_counts[y][i][excluded_index] += increment
        for j in range(9):
            self.exclusion_counts[j][x][excluded_index] += increment
        for i in range(x // 3 * 3, x // 3 * 3 + 3):
            for j in range(y // 3 * 3, y // 3 * 3 + 3):
                self.exclusion_counts[j][i][excluded_index] += increment

        self.board[y][x] = value

    @property
    def full(self):
        return all(value is not None for row in self.board for value in row)

    @property
    def solved(self):
        rows_good = all(set(row) == set(range(1, 10)) for row in self.board)
        cols = [[self.board[y][x] for x in range(9)] for y in range(9)]
        cols_good = all(set(col) == set(range(1, 10)) for col in cols)
        squares = [[
            self.board[y][x]
            for x in range(i, i + 3)
            for y in range(j, j + 3)
        ] for i in range(9, 3) for j in range(9, 3)]
        squares_good = all(
            set(square) == set(range(1, 10)) for square in squares
        )
        return rows_good and cols_good and squares_good

    @property
    def empty_squares(self):
        return [
            (x, y) for x in range(9) for y in range(9)
            if self.board[y][x] is None
        ]

    def moves_for_square(self, x, y):
        counts = self.exclusion_counts[y][x]
        return [i + 1 for (i, count) in enumerate(counts) if count == 0]

    def __str__(self):
        def group_and_join(values, group_size, group_separator, joiner):
            tokens = []
            for i, value in enumerate(values):
                if i % group_size == 0:
                    tokens.append(group_separator)
                tokens.append(value)
            tokens.append(group_separator)
            return joiner.join(tokens)

        def row_string(row):
            values = [str(value) if value is not None else "." for value in row]
            return group_and_join(values, 3, "|", " ")

        rows = [row_string(row) for row in self.board]
        row_separator =  "+-------+-------+-------+"
        return group_and_join(rows, 3, row_separator, "\n") + "\n"

    def __eq__(self, other):
        return self.board == other.board


def solve(board):
    return BacktrackingSudokuSolver().solve(board)
