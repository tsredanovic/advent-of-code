import io
import os
from pydoc import locate

import settings

from aocd import get_data

class NotImplementedError(Exception):
    pass

class Solver:
    def __init__(self, year, day, part, test=False, test_data_path=None):
        self.year = year
        self.day = day
        self.part = part
        self.test = test
        self.test_data_path = test_data_path
        self.data = get_data(year=year, day=day) if not test else self.get_test_data(test_data_path)

    def get_test_data(self, test_data_path):
        with io.open(os.path.join(settings.AOCTD_DIR, test_data_path), encoding="utf-8") as f:
            data = f.read()

        return data.rstrip("\r\n")
    
    def get_solver(self):
        module_name = 'y{}d{:02d}'.format(self.year, self.day)
        class_name = 'Y{}D{:02d}Solver'.format(self.year, self.day)

        solver_class = locate('solvers.{}.{}'.format(module_name, class_name))

        return solver_class

    def solve(self, print_solution=False):
        Solver = self.get_solver()
        solver = Solver(self.data, self.part)
        if self.part == 'a':
            solution = solver.solve_part_a()
        elif self.part == 'b':
            solution = solver.solve_part_b()
        
        if print_solution:
            test_str = '.{}'.format(self.test_data_path) if self.test else ''
            print('{}.{}.{:02d}.{}{} -> {}'.format(
                'TEST' if self.test else 'REAL',
                self.year, 
                self.day, 
                self.part,
                test_str ,
                solution
                )
            )
        
        return solution
