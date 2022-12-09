from advent_of_code.basesolver import BaseSolver


class Y2021D07Solver(BaseSolver):
    def solve_part_a(self):
        positions = [int(i) for i in self.lines[0].split(",")]
        min_cost = 9999999999999
        min_cost_pos = None
        for possible_pos in range(min(positions), max(positions) + 1):
            possible_pos_cost = 0
            for pos in positions:
                possible_pos_cost += abs(pos - possible_pos)

            if possible_pos_cost < min_cost:
                min_cost = possible_pos_cost
                min_cost_pos = possible_pos

        return min_cost

    def solve_part_b(self):
        positions = [int(i) for i in self.lines[0].split(",")]
        print("Min: {}".format(min(positions)))
        print("Max: {}".format(max(positions) + 1))
        min_cost = 9999999999999
        min_cost_pos = None
        for possible_pos in range(min(positions), max(positions) + 1):
            print("Calc: {}".format(possible_pos))
            possible_pos_cost = 0
            for pos in positions:
                moves = abs(pos - possible_pos)
                for i in range(1, moves + 1):
                    possible_pos_cost += i

            if possible_pos_cost < min_cost:
                min_cost = possible_pos_cost
                min_cost_pos = possible_pos

        return min_cost
