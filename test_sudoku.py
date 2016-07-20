import cProfile
import logging
import unittest

from sudoku import SudokuBoard, solve


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class TestSudokuSolver(unittest.TestCase):
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
        expected = SudokuBoard([
            [6, 7, 3, 8, 9, 4, 5, 1, 2],
            [9, 1, 2, 7, 3, 5, 4, 8, 6],
            [8, 4, 5, 6, 1, 2, 9, 7, 3],
            [7, 9, 8, 2, 6, 1, 3, 5, 4],
            [5, 2, 6, 4, 7, 3, 8, 9, 1],
            [1, 3, 4, 5, 8, 9, 2, 6, 7],
            [4, 6, 9, 1, 2, 8, 7, 3, 5],
            [2, 8, 7, 3, 5, 6, 1, 4, 9],
            [3, 5, 1, 9, 4, 7, 6, 2, 8],
        ])
        logger.debug(board)
        solution = solve(board)
        logger.debug(solution)
        self.assertEqual(solution, expected)

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
        expected = SudokuBoard([
            [8, 1, 2, 7, 5, 3, 6, 4, 9],
            [9, 4, 3, 6, 8, 2, 1, 7, 5],
            [6, 7, 5, 4, 9, 1, 2, 8, 3],
            [1, 5, 4, 2, 3, 7, 8, 9, 6],
            [3, 6, 9, 8, 4, 5, 7, 2, 1],
            [2, 8, 7, 1, 6, 9, 5, 3, 4],
            [5, 2, 1, 9, 7, 4, 3, 6, 8],
            [4, 3, 8, 5, 2, 6, 9, 1, 7],
            [7, 9, 6, 3, 1, 8, 4, 5, 2],
        ])
        logger.debug(board)
        solution = solve(board)
        logger.debug(solution)
        self.assertEqual(solution, expected)


if __name__ == '__main__':
    suite = unittest.TestLoader().discover('.')
    def runtests():
        unittest.TextTestRunner().run(suite)
    s = cProfile.run('runtests()', sort='tottime')
