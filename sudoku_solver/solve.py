import pulp
import sys


class Solve(object):

    def __init__(self, grid):
        self.grid = grid
        self.r = 0
        self.c = 0

    def solve_sudoku(self):
        if self._solve_sudoku():
            solved_grid = self.grid
            return solved_grid
        else:
            return "No Solution Exists"

    def _solve_sudoku(self):
        self.r, self.c = 0, 0
        if not self._find_empty_cell():
            return True

        row = self.r
        col = self.c

        for num in range(1, 10):
            if self._check_valid_loc(row, col, num):
                self.grid[row][col] = num

                if self._solve_sudoku():
                    return True

                self.grid[row][col] = 0

        return False

    def _find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    self.r = i
                    self.c = j
                    return True
        return False

    def _check_valid_loc(self, row, col, num):
        row_present = self._is_present_in_row(row, num)
        col_present = self._is_present_in_col(col, num)
        box_present = self._is_present_in_box((row - row % 3), (col - col % 3), num)

        return not row_present and not col_present and not box_present

    def _is_present_in_row(self, row, num):
        for i in range(9):
            if self.grid[row][i] == num:
                return True
        return False

    def _is_present_in_col(self, col, num):
        for i in range(9):
            if self.grid[i][col] == num:
                return True
        return False

    def _is_present_in_box(self, row, col, num):
        for i in range(3):
            for j in range(3):
                if self.grid[row + i][col + i] == num:
                    return True
        return False
