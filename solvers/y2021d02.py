
from basesolver import BaseSolver


class Y2021D02Solver(BaseSolver):
    def solve_part_a(self):
        horizontal = 0
        depth = 0

        for line in self.lines:
            direction, num = line.split()
            num = int(num)
            if direction == 'forward':
                horizontal += num
            elif direction == 'up':
                depth -= num
            elif direction == 'down':
                depth += num

        return horizontal * depth
    

    def solve_part_b(self):
        horizontal = 0
        depth = 0
        aim = 0

        for line in self.lines:
            direction, num = line.split()
            num = int(num)
            if direction == 'forward':
                horizontal += num
                depth += aim * num
            elif direction == 'up':
                aim -= num
            elif direction == 'down':
                aim += num
        return horizontal * depth

