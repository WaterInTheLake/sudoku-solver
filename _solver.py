import itertools
import numpy as np

class Mixin:

    def run_singles(self, loops):
        """
        Any cells which have only one candidate
        can safely be assigned that value
        """
        while loops:
            loops -= 1
            self.iteration_routine_start("Singles")

            for row, col in itertools.product(range(0, 9), repeat=2):
                candidates = self.candidates[row][col]
                if isinstance(candidates, list):
                    if len(candidates) == 1:
                        self.solved_cell(row, col, candidates[0])

        self.iteration_routine_end()

    def run_hidden_singles_row(self, loops):
        """
        If there is only one unique candidate in a cell for a given row
        it can safely be assigned that value
        """
        while loops:
            loops -= 1
            self.iteration_routine_start("Hidden Row")

            for row in range(0, 9):
                candidate_dict = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}
                for col, candidates in enumerate(self.candidates[row]): # fetch row
                    if isinstance(candidates, list): # If current iteration is not solved
                        for value in candidates:
                            candidate_dict[value] += str(col)

                for value in candidate_dict:
                    if len(candidate_dict[value]) == 1: # If a number has a unique square, it must belong there
                        candidate_col = int(candidate_dict[value])
                        self.solved_cell(row, candidate_col, value)

            self.iteration_routine_end()

    def run_hidden_singles_col(self, loops):
        """
        If there is only one unique candidate in a cell for a given column
        it can safely be assigned that value
        """
        while loops:
            loops -= 1
            self.iteration_routine_start("Hidden Column")

            for col in range(0, 9):
                candidate_dict = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}
                for row, candidates in enumerate([R[col] for R in self.candidates]): # fetch column
                    if isinstance(candidates, list): # If current iteration is not solved
                        for value in candidates:
                            candidate_dict[value] += str(row)

                for value in candidate_dict:
                    if len(candidate_dict[value]) == 1: # If a number has a unique square, it must belong there
                        candidate_row = int(candidate_dict[value])
                        self.solved_cell(candidate_row, col, value)

            self.iteration_routine_end()

    def run_hidden_singles_quad(self, loops):
        """
        If there is only one unique candidate in a cell for a given quadrant
        it can safely be assigned that value
        """
        while loops:
            loops -= 1
            self.iteration_routine_start("Hidden Quad")

            for Mrow in (0, 3, 6):
                for Mcol in (0, 3, 6):
                    quadrant = self.generate_quadrant(Mrow, Mcol, replace_solved=True)

                    candidate_dict = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}

                    for cell, candidates in enumerate(quadrant):
                        for value in candidates:
                            candidate_dict[value] += str(cell)

                    for value in candidate_dict:
                        if len(candidate_dict[value]) == 1: # If a number has a unique square, it must belong there
                            candidate_row = Mrow + int(candidate_dict[value]) // 3
                            candidate_col = Mcol + int(candidate_dict[value]) % 3
                            self.solved_cell(candidate_row, candidate_col, value)

            self.iteration_routine_end()

    def run_locked_candidate_row_col(self, loops):
        """
        If a candidate only exists in a single row or column witihin a quadrant,
        then the candidate can safely be excluded from the remaining cells
        in that row or column outside of the quadrant.
        """
        while loops:
            loops -= 1
            self.iteration_routine_start("Locked Candidate Row Col")

            correct_pattern = ([0, 0, 2], [0, 0, 3])

            # For each quadrant
            for Mrow in (0, 3, 6):
                for Mcol in (0, 3, 6):

                    # For 1, 2, 3, ..., 9
                    for candidate_value in range(1, 10):
                        quadrant = self.generate_quadrant(Mrow, Mcol, replace_solved=True)
                        occurences_per_row = []
                        occurences_per_col = []

                        # If value to check is NOT amongst the candidates in this quadrant
                        if candidate_value not in itertools.chain.from_iterable(quadrant):
                            continue

                        # List with number of times value occures per ROW within quadrant
                        # If match, we have a locked candidate
                        for Qrow in (0, 3, 6):
                            Qrow_candidates = quadrant[Qrow:Qrow+3]
                            occurences_per_row.append(list(itertools.chain.from_iterable(Qrow_candidates)).count(candidate_value))
                        if sorted(occurences_per_row) in correct_pattern:
                            row = int(Mrow + np.nonzero(occurences_per_row)[0][0])
                            self.solved_locked_candidate_row_col(Mrow, Mcol, candidate_value, Crow=row)
                            # If match, no need to check columns
                            continue

                        # List with number of times value occures per COLUMN within quadrant
                        # If match, we have a locked candidate
                        for Qcol in (0, 1, 2):
                            Qcol_candidates = list(quadrant[C] for C in (Qcol, Qcol+3, Qcol+6))
                            occurences_per_col.append(list(itertools.chain.from_iterable(Qcol_candidates)).count(candidate_value))
                        if sorted(occurences_per_col) in correct_pattern:
                            col = int(Mcol + np.nonzero(occurences_per_col)[0][0])
                            self.solved_locked_candidate_row_col(Mrow, Mcol, candidate_value, Ccol=col)

            self.iteration_routine_end()

    def run_locked_candidate_quad(self, loops):
        """
        If a candidate only exists in a single quadrant witihin a row or column,
        then the candidate can safely be excluded from the remaining cells
        in that quadrant.
        """
        while loops:
            loops -= 1
            self.iteration_routine_start("Locked Candidate Quad")

            correct_pattern = ([0, 0, 2], [0, 0, 3])

            for row in range(0, 9):
                row_elems = [elem if isinstance(elem, list) else [] for elem in self.candidates[row]]
                for candidate_value in range(1, 10):
                    occurences = []

                    # If value to check is NOT amongst the candidates in this quadrant
                    if candidate_value not in itertools.chain.from_iterable(row_elems):
                        continue

                    for Q in (0, 3, 6):
                        occurences.append(list(itertools.chain.from_iterable(row_elems[Q:Q+3])).count(candidate_value))

                    # If match, we have a locked candidate
                    if sorted(occurences) in correct_pattern:
                        Mrow = (row // 3) * 3
                        Mcol = int(np.nonzero(occurences)[0][0] * 3)
                        self.solved_locked_candidate_quad(Mrow, Mcol, candidate_value, Crow=row)

            for col in range(0, 9):
                col_elems = []
                for R in self.candidates:
                    if isinstance(R[col], list):
                        col_elems.append(R[col])
                    else:
                        col_elems.append([])
                for candidate_value in range(1, 10):
                    occurences = []

                    # If value to check is NOT amongst the candidates in this quadrant
                    if candidate_value not in itertools.chain.from_iterable(col_elems):
                        continue

                    for Q in (0, 3, 6):
                        occurences.append(list(itertools.chain.from_iterable(col_elems[Q:Q+3])).count(candidate_value))

                    # If match, we have a locked candidate
                    if sorted(occurences) in correct_pattern:
                        Mrow = int(np.nonzero(occurences)[0][0] * 3)
                        Mcol = (col // 3) * 3
                        self.solved_locked_candidate_quad(Mrow, Mcol, candidate_value, Ccol=col)

            self.iteration_routine_end()

    def solved_cell(self, row, col, value):
        """
        Set cell to solved in self.puzzle and self.candidates
        Remove value from all related candidates list
        """
        self.puzzle[row][col] = int(value)
        self.candidates[row][col] = int(value)

        related_coordinates = self.return_related_coordinates(row, col)
        for cell in related_coordinates:
            Crow, Ccol = int(cell[0]), int(cell[1])
            candidates = self.candidates[Crow][Ccol]
            if isinstance(candidates, list):
                if len(candidates) >= 2:
                    if value in candidates:
                        self.candidates[Crow][Ccol].remove(value)

    def solved_locked_candidate_row_col(self, Mrow, Mcol, value, Crow=None, Ccol=None):
        """
        Excluded candidate value from the remaining cells
        in that row or column OUTSIDE of the quadrant.
        """
        removed = 0
        # If candidates is on a row
        if isinstance(Crow, int):
            columns = [elem for elem in range(0, 9) if elem not in (Mcol, Mcol+1, Mcol+2)]

            for col in columns:
                cell = self.candidates[Crow][col]
                if isinstance(cell, list):
                    if value in cell:
                        removed += 1
                        self.candidates[Crow][col].remove(value)

        # If candidates is in a column
        if isinstance(Ccol, int):
            rows = [elem for elem in range(0, 9) if elem not in (Mrow, Mrow+1, Mrow+2)]

            for row in rows:
                cell = self.candidates[row][Ccol]
                if isinstance(cell, list):
                    if value in cell:
                        removed += 1
                        self.candidates[row][Ccol].remove(value)

        if removed and self.verbose:
            print(Mrow, Mcol, "VALUE", value, "REMOVED", removed)

    def solved_locked_candidate_quad(self, Mrow, Mcol, value, Crow=None, Ccol=None):
        """
        Excluded candidate value from the remaining cells
        in remaining row or column INSIDE of the quadrant.
        """
        removed = 0
        # If candidates is on a row
        if isinstance(Crow, int):
            rows = [elem for elem in range(Mrow, Mrow+3) if elem != Crow]

            for row in rows:
                for col in range(Mcol, Mcol+3):
                    cell = self.candidates[row][col]
                    if isinstance(cell, list):
                        if value in cell:
                            removed += 1
                            self.candidates[row][col].remove(value)

        # If candidates is in a column
        if isinstance(Ccol, int):
            cols = [elem for elem in range(Mcol, Mcol+3) if elem != Ccol]

            for row in range(Mrow, Mrow+3):
                for col in cols:
                    cell = self.candidates[row][col]
                    if isinstance(cell, list):
                        if value in cell:
                            removed += 1
                            self.candidates[row][col].remove(value)

        if removed and self.verbose:
            print(Mrow, Mcol, "VALUE", value, "REMOVED", removed)

