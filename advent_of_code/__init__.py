import argparse
import importlib
from pathlib import Path
from aocd import get_data

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent


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

    # Get data
    solver_dir = BASE_DIR / str(args.year) / '{:02d}'.format(args.day)
    if args.data:
        # Get test data
        data_id = args.data
        if data_id.isdigit():
            data_id = '{}_{:02d}_{}_input.txt'.format(args.year, args.day, data_id)
        data_path = solver_dir / 'data' / data_id
        with open(data_path, 'r') as f:
            data = f.read()
    else:
        # Get real data
        data = get_data(year=args.year, day=args.day)
    
    # Get solver
    module_name = '{}.{}.{:02d}.y{}d{:02d}'.format(BASE_DIR.name, args.year, args.day, args.year, args.day)
    module = importlib.import_module(module_name)
    class_name = 'Y{}D{:02d}Solver'.format(args.year, args.day)
    class_ = getattr(module, class_name)
    solver = class_(data, args.part)

    # Solve
    if args.part == 'a':
        solution = solver.solve_part_a()
    elif args.part == 'b':
        solution = solver.solve_part_b()

    print(solution)


def generate_empty_solvers():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='year')
    args = parser.parse_args()

    import pdb
    pdb.set_trace()