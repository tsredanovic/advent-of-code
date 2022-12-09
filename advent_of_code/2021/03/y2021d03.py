import pprint

from advent_of_code.basesolver import BaseSolver


def get_bit_counts(lines):
    bit_counts = {}
    for i in range(len(lines[0])):
        bit_counts[i] = {0: 0, 1: 0}

    for line in lines:
        for i in range(len(line)):
            bit = int(line[i])
            bit_counts[i][bit] += 1

    return bit_counts


class Y2021D03Solver(BaseSolver):
    def solve_part_a(self):
        bit_counts = {}
        for i in range(len(self.lines[0])):
            bit_counts[i] = {0: 0, 1: 0}

        for line in self.lines:
            for i in range(len(line)):
                bit = int(line[i])
                bit_counts[i][bit] += 1

        gamma_rate = []
        epsilon_rate = []
        for i in range(len(self.lines[0])):
            gamma_rate.append("0" if bit_counts[i][0] > bit_counts[i][1] else "1")
            epsilon_rate.append("0" if bit_counts[i][0] < bit_counts[i][1] else "1")
        return int("".join(gamma_rate), 2) * int("".join(epsilon_rate), 2)

    def solve_part_b(self):
        current_stack = self.lines.copy()
        current_bit_counts = get_bit_counts(current_stack)
        for i in range(len(self.lines[0])):
            bit_to_keep = (
                "0" if current_bit_counts[i][0] > current_bit_counts[i][1] else "1"
            )
            new_stack = []
            for line in current_stack:
                if line[i] == bit_to_keep:
                    new_stack.append(line)
            current_stack = new_stack
            current_bit_counts = get_bit_counts(current_stack)
            if len(current_stack) == 1:
                break

        oxygen_generator_rating = current_stack[0]

        current_stack = self.lines.copy()
        current_bit_counts = get_bit_counts(current_stack)
        for i in range(len(self.lines[0])):
            bit_to_keep = (
                "1" if current_bit_counts[i][0] > current_bit_counts[i][1] else "0"
            )
            new_stack = []
            for line in current_stack:
                if line[i] == bit_to_keep:
                    new_stack.append(line)
            current_stack = new_stack
            current_bit_counts = get_bit_counts(current_stack)
            if len(current_stack) == 1:
                break

        co2_scrubber_rating = current_stack[0]

        return int("".join(oxygen_generator_rating), 2) * int(
            "".join(co2_scrubber_rating), 2
        )
