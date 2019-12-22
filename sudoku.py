import _solver
import csv
import numpy as np
import random
from tabulate import tabulate



class Sudoku(_solver.Mixin):
    def __init__(self, random_sudoku=True, verbose=True):
        self.random_sudoku = random_sudoku
        self.puzzle, self.solution = self.fetch_puzzle()
        self.candidates = [["" for x in range(9)] for y in range(9)]
        self.calc_all_candidates()
        self.iterations = 0
        self.left_to_solve = 81
        self.verbose = verbose

    def iteration_routine_start(self, message):
        self.iterations += 1
        self.left_to_solve = 81-np.count_nonzero(self.puzzle)
        if self.verbose:
            print("Start: ", self.iterations, "     Left to solve: ", self.left_to_solve, "    ", message)

    def iteration_routine_end(self):
        self.left_to_solve = 81-np.count_nonzero(self.puzzle)
        if self.verbose:
            print("End:   ", self.iterations, "                    ", self.left_to_solve, "    ")

    def prettyprint(self, what="puzzle", lining=True):
        """
        Prints puzzle (or solution) to screen in a
        more readable format
        """
        if what == "solution":
            M = self.solution
        elif what == "candidates":
            M = self.candidates
            print(tabulate(self.candidates, tablefmt="fancy_grid", headers="012345678"))
            return None
        else:
            M = self.puzzle
        print("--- {} ---".format(type))
        for i, row in enumerate(M):
            for j, digit in enumerate(row):
                if j in (2, 5):
                    if lining:
                        print(digit, end=" | ")
                    else:
                        print(digit, end=" ")
                elif j == 8:
                    print(digit)
                else:
                    print(digit, end=" ")
            if lining:
                if i in (2, 5):
                    print("------+-------+------")
        print("")
        return None

    def calc_all_candidates(self):
        for row, col in np.ndindex(self.puzzle.shape):
            if self.puzzle[row][col] == 0:
                self.candidates[row][col] = self.return_candidates(row, col)
            else:
                self.candidates[row][col] = int(self.puzzle[row][col])

    def check_solution(self):
        correct = True

        for row, col in np.ndindex(self.puzzle.shape):
            if self.puzzle[row][col] != 0:
                if self.puzzle[row][col] != self.solution[row][col]:
                    correct = False

        if correct:
            if self.verbose:
                print("---PASSED---\n")
            return True
        else:
            if self.verbose:
                print("---FAILED---\n")
            return False

    def fetch_puzzle(self):
        """
        Fetch a sudoku from a file containing 1 million different puzzles
        """
        with open('data/sudoku_own.csv', newline='') as f:
            reader = csv.reader(f)
            row_count = sum(1 for row in reader)
            f.seek(0)
            next(reader) # discard header

            if self.random_sudoku:
                for i in range(random.randrange(0, row_count-1)):
                    next(reader) # discard rows
            else:
                pass

            puzzle, solution, comment = next(reader)
            puzzle, solution, comment = next(reader)
            # print("Pussel:", comment)

            puzzle = np.fromiter((number for number in puzzle), dtype=int).reshape(9,9)
            solution = np.fromiter((number for number in solution), dtype=int).reshape(9,9)

            return puzzle, solution

    def generate_quadrant(self, Mrow, Mcol, replace_solved=False):
        quadrant = []
        for Qrow in self.candidates[Mrow:Mrow+3]:
            for candidates in (Qrow[Mcol:Mcol+3]):
                if replace_solved:
                    if isinstance(candidates, list):
                        quadrant.append(candidates)
                    else:
                        quadrant.append([])
                else:
                    quadrant.append(candidates)
        return(quadrant)

    def return_related(self, row, col):
        """
        Return related numbers in
        [Horizontal, Vertical, Quadrant] order
        """

        M = self.puzzle
        Mrow = row//3*3
        Mcol = col//3*3

        hor = M[row]
        ver = M[:, col]
        quad = M[[Mrow,Mrow+1,Mrow+2]][:,[Mcol,Mcol+1,Mcol+2]].flatten()

        output = np.vstack((hor, ver, quad))

        return output

    def return_related_coordinates(self, row, col):
        """
        Return related coordinates in
        set("04", "10", ..., "16"), unordered
        """

        M = self.puzzle
        Mrow = row//3*3
        Mcol = col//3*3

        hor = [str(row)+str(elem) for elem in range(0,9)]
        ver = [str(elem)+str(col) for elem in range(0,9)]
        quad = [str(Qrow)+str(Qcol) for Qrow in range(Mrow, Mrow+3) for Qcol in range(Mcol, Mcol+3)]

        output = set(hor + ver + quad)

        return output

    def return_candidates(self, row, col):
        possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        not_possible = np.unique(self.return_related(row, col))
        return list(set(possible) - set(not_possible))

    def run(self):

        loops = 3


        while loops:
            loops -= 1
            self.run_singles(1) #
            self.run_locked_candidate_row_col(1)
            self.run_locked_candidate_quad(1) #
            self.run_hidden_singles_quad(1) #
            self.run_hidden_singles_row(1) #
            self.run_hidden_singles_col(1) #

        # self.prettyprint(what="candidates")

        self.check_solution()

if __name__ == '__main__':
    sudoku = Sudoku(random_sudoku=False, verbose=False)
    # sudoku.prettyprint()
    sudoku.run()
    # sudoku.prettyprint(what="candidates")
    # sudoku.prettyprint()
    # sudoku.prettyprint(what="solution")
    exec(open("test_sudoku.py").read())
