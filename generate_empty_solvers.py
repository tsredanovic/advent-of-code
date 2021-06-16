import os

DIR = '/Users/tonisredanovic/Projects/advent-of-code/solvers/'

years = [2020, 2019, 2018, 2017, 2016]
days = [day for day in range(1, 26)]

file_content_template = """
from basesolver import BaseSolver


class Y{}D{:02d}Solver(BaseSolver):
    def solve_part_a(self):
        return None
    

    def solve_part_b(self):
        return None

"""

for year in years:
    for day in days:
        file_name = 'y{}d{:02d}.py'.format(year, day)
        print(file_name)

        file_path = os.path.join(DIR, file_name)
        if os.path.isfile(file_path):
            print('\tExists.')
            continue

        file_content = file_content_template.format(year, day)
        with open(file_path, 'w+') as f:
            f.write(file_content)
        print('\tCreated.')
