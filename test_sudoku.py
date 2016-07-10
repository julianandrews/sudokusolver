import logging
import unittest

from sudoku import SudokuBoard, solve


logger = logging.getLogger("SudokuSolverTests")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class TestSudokuSolver(unittest.TestCase):
    def board_test(self, board):
        logger.debug("\n{}".format(board))
        solution = solve(board)
        logger.debug(solution)
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
