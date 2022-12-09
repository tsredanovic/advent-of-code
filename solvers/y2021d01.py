from advent_of_code.basesolver import BaseSolver


class Y2021D01Solver(BaseSolver):
    def solve_part_a(self):
        increase_count = 0
        for i in range(1, len(self.numbers)):
            if self.numbers[i] > self.numbers[i-1]:
                increase_count += 1
        return increase_count

    def solve_part_b(self):
        increase_count = 0
        for i in range(3, len(self.numbers)):
            first_window_sum = self.numbers[i-3] + self.numbers[i-2] + self.numbers[i-1]
            second_window_sum = self.numbers[i-2] + self.numbers[i-1] + self.numbers[i]
            if second_window_sum > first_window_sum:
                increase_count += 1
        return increase_count