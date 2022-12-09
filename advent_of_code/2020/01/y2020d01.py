import itertools

from advent_of_code.basesolver import BaseSolver


class Y2020D01Solver(BaseSolver):
    def solve_part_a(self):
        result = None
        for combination in itertools.combinations(self.numbers, 2):
            if combination[0] + combination[1] == 2020:
                result = combination[0] * combination[1]
                break

        return str(result)

    def solve_part_b(self):
        result = None
        for combination in itertools.combinations(self.numbers, 3):
            if combination[0] + combination[1] + combination[2] == 2020:
                result = combination[0] * combination[1] * combination[2]
                break

        return str(result)
