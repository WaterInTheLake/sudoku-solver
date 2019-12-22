from sudoku import Sudoku
import itertools
import unittest

class TestSudoku(unittest.TestCase):

    def setUp(self):
        self.sudoku = Sudoku(random_sudoku=False, verbose=False)

    def test_fetch_puzzle(self):
        self.assertEqual(self.sudoku.puzzle[0][0], 3)
        self.assertEqual(self.sudoku.puzzle[8][8], 1)
        self.assertEqual(len(list(itertools.chain.from_iterable(self.sudoku.puzzle))), 81)

    def test_run_singles(self):
        self.sudoku.run_locked_candidate_quad(1)
        self.sudoku.run_singles(1)
        self.assertEqual(self.sudoku.left_to_solve, 24)

    def test_run_other_solvers(self):
        loops = 3

        while loops:
            loops -= 1
            self.sudoku.run_singles(1) #
            self.sudoku.run_locked_candidate_row_col(1)
            self.sudoku.run_locked_candidate_quad(1) #
            self.sudoku.run_hidden_singles_quad(1) #
            self.sudoku.run_hidden_singles_row(1) #
            self.sudoku.run_hidden_singles_col(1) #

        self.assertEqual(self.sudoku.left_to_solve, 1)
        self.assertTrue(self.sudoku.check_solution())

if __name__ == '__main__':
    unittest.main()
