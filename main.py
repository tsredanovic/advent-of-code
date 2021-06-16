import sys

from solver import Solver

# Read args
year = int(sys.argv[1])
day = int(sys.argv[2])
part = sys.argv[3]
test_data_path = sys.argv[4] if len(sys.argv) > 4 else None

# Solve
solver = Solver(
    year=year, 
    day=day, 
    part=part, 
    test=True if test_data_path else False, 
    test_data_path=test_data_path
)

solution = solver.solve(print_solution=True)
