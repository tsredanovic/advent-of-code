import argparse
import importlib
from pathlib import Path
from aocd import get_data

from dotenv import load_dotenv

class Solver:
    def __init__(self, year, day, part, data_id):
        self.year = year
        self.day = day
        self.part = part

        self.base_dir = Path(__file__).resolve().parent
        self.solver_dir = self.base_dir / str(year) / '{:02d}'.format(day)

        self.data = get_data(year=year, day=day) if not data_id else self.get_test_data(data_id)

    def get_test_data(self, data_id):
        if data_id.isdigit():
            data_id = '{}_{:02d}_{}_input.txt'.format(self.year, self.day, data_id)
        data_path = self.solver_dir / 'data' / data_id
        with open(data_path, 'r') as f:
            return f.read()
    
    def get_solver_class(self):
        module_name = '{}.{}.{:02d}.y{}d{:02d}'.format(self.base_dir.name, self.year, self.day, self.year, self.day)
        module = importlib.import_module(module_name)

        class_name = 'Y{}D{:02d}Solver'.format(self.year, self.day)

        return getattr(module, class_name)

    def solve(self):
        Solver = self.get_solver_class()
        solver = Solver(self.data, self.part)
        if self.part == 'a':
            solution = solver.solve_part_a()
        elif self.part == 'b':
            solution = solver.solve_part_b()

        return solution

def solve():
    # Env vars
    load_dotenv()

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='year')
    parser.add_argument('day', type=int, help='day', choices=range(1, 26))
    parser.add_argument('part', type=str, choices=['a', 'b'], help='part')
    parser.add_argument('-d', '--data', required=False)
    args = parser.parse_args()

    # Solve
    solver = Solver(args.year, args.day, args.part, args.data)
    result = solver.solve()
    print(result)
