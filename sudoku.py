import logging
import unittest


class BacktrackingSolver:
    def solve(self, state):
        if self.is_a_solution(state):
            return state

        for move in self.get_candidates(state):
            self.make_move(move, state)
            solution = self.solve(state)
            if solution:
                return solution
            else:
                self.unmake_move(move, state)

        return None

    def is_a_solution(self, state):
        raise NotImplemented

    def get_candidates(self, state):
        raise NotImplemented

    def make_move(self, move, state):
        raise NotImplemented

    def unmake_move(self, move, state):
        raise NotImplemented


class BacktrackingSudokuSolver(BacktrackingSolver):
    def is_a_solution(self, board):
        return board.full

    def get_candidates(self, board):
        possible_moves = [(x, y, board.moves_for_square(x, y)) for x, y in board.empty_squares]
        x, y, values = min(possible_moves, key=lambda args: len(args[2]))
        return [(x, y, value) for value in values]

    def make_move(self, move, board):
        x, y, value = move
        board.set_value(x, y, value)

    def unmake_move(self, move, board):
        x, y, value = move
        board.set_value(x, y, None)


class SudokuBoard:
    def __init__(self, board):
        self.board = board

    def set_value(self, x, y, value):
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
        squares_good = all(set(square) == set(range(1, 10)) for square in squares)
        return rows_good and cols_good and squares_good

    @property
    def empty_squares(self):
        return (
            (x, y) for x in range(9) for y in range(9)
            if self.board[y][x] is None
        )

    def moves_for_square(self, x, y):
        row_values = self.board[y]
        column_values = [self.board[j][x] for j in range(9)]
        square_values = [
            self.board[j][i]
            for i in range(x // 3 * 3, x // 3 * 3 + 3)
            for j in range(y // 3 * 3, y // 3 * 3 + 3)
        ]
        return [
            value for value in (1, 2, 3, 4, 5, 6, 7, 8, 9)
            if not value in row_values
            and not value in column_values
            and not value in square_values
        ]

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
            values = [str(value) if value is not None else " " for value in row]
            return group_and_join(values, 3, "|", " ")

        return group_and_join(
            map(row_string, self.board), 3, "+-------+-------+-------+", "\n"
        ) + "\n"

    def __eq__(self, other):
        return self.board == other.board


def solve(board):
    return BacktrackingSudokuSolver().solve(board)


class TestSudokuSolver(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.logger = logging.getLogger("TestSudokuSolver")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

    def board_test(self, board):
        self.logger.debug("\n{}".format(board))
        solution = solve(board)
        self.logger.debug(solution)
        assert solution.solved

    def test_easy_board(self):
        board = SudokuBoard([
            [None, None, None, None, None, None, None, 1, 2],
            [None, None, None, None, 3, 5, None, None, None],
            [None, None, None, 6, None, None, None, 7, None],
            [7, None, None, None, None, None, 3, None, None],
            [None, None, None, 4, None, None, 8, None, None],
            [1, None, None, None, None, None, None, None, None],
            [None, None, None, 1, 2, None, None, None, None],
            [None, 8, None, None, None, None, None, 4, None],
            [None, 5, None, None, None, None, 6, None, None],
        ])
        self.board_test(board)

    def test_hard_board(self):
        board = SudokuBoard([
            [8, None, None, None, None, None, None, None, None],
            [None, None, 3, 6, None, None, None, None, None],
            [None, 7, None, None, 9, None, 2, None, None],
            [None, 5, None, None, None, 7, None, None, None],
            [None, None, None, None, 4, 5, 7, None, None],
            [None, None, None, 1, None, None, None, 3, None],
            [None, None, 1, None, None, None, None, 6, 8],
            [None, None, 8, 5, None, None, None, 1, None],
            [None, 9, None, None, None, None, 4, None, None],
        ])
        self.board_test(board)


if __name__ == '__main__':
    unittest.main()
