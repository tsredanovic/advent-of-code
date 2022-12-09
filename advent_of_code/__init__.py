import argparse
import importlib
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent


def solve():
    # Env vars
    load_dotenv()
    from aocd import get_data

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, help="year")
    parser.add_argument("day", type=int, help="day", choices=range(1, 26))
    parser.add_argument("part", type=str, choices=["a", "b"], help="part")
    parser.add_argument("-d", "--data", required=False)
    args = parser.parse_args()

    # Get data
    solver_dir = BASE_DIR / str(args.year) / "{:02d}".format(args.day)
    if args.data:
        # Get test data
        data_id = args.data
        if data_id.isdigit():
            data_id = "{}_{:02d}_{}_input.txt".format(args.year, args.day, data_id)
        data_path = solver_dir / "data" / data_id
        with data_path.open("r", encoding="utf-8") as f:
            data = f.read()
            data.rstrip("\r\n")
    else:
        # Get real data
        data = get_data(year=args.year, day=args.day)

    # Get solver
    module_name = "{}.{}.{:02d}.y{}d{:02d}".format(
        BASE_DIR.name, args.year, args.day, args.year, args.day
    )
    module = importlib.import_module(module_name)
    class_name = "Y{}D{:02d}Solver".format(args.year, args.day)
    class_ = getattr(module, class_name)
    solver = class_(data, args.part)

    # Solve
    if args.part == "a":
        solution = solver.solve_part_a()
    elif args.part == "b":
        solution = solver.solve_part_b()

    print(solution)


def generate_empty_solvers():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, help="year")
    args = parser.parse_args()

    # Template
    file_content_template = """from advent_of_code.basesolver import BaseSolver


class Y{}D{:02d}Solver(BaseSolver):
    def solve_part_a(self):
        return None
    

    def solve_part_b(self):
        return None
"""

    # Create
    for day in range(1, 26):
        solver_file_path = (
            BASE_DIR
            / str(args.year)
            / "{:02d}".format(day)
            / "y{}d{:02d}.py".format(args.year, day)
        )

        data_dir = solver_file_path.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        if solver_file_path.is_file():
            print("Day {:02d} structure exists.".format(day))
        else:
            with solver_file_path.open("w", encoding="utf-8") as f:
                f.write(file_content_template.format(args.year, day))
            print("Day {:02d} structure created.".format(day))
