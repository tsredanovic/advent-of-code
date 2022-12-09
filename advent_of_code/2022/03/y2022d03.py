import string

from advent_of_code.basesolver import BaseSolver


class CharPriorityManager:
    def __init__(self) -> None:
        chars = string.ascii_lowercase + string.ascii_uppercase
        self.priorities = {}
        for i, char in enumerate(chars):
            char = chars[i]
            self.priorities[char] = i + 1

    def get(self, char):
        return self.priorities[char]


class Y2022D03Solver(BaseSolver):
    def solve_part_a(self):
        priorities = CharPriorityManager()
        priorities_sum = 0
        for line in self.lines:
            first_part, second_part = line[: len(line) // 2], line[len(line) // 2 :]
            intersection_chars = set(first_part).intersection(set(second_part))
            for char in intersection_chars:
                char_priority = priorities.get(char)
                priorities_sum += char_priority
        return priorities_sum

    def solve_part_b(self):
        priorities = CharPriorityManager()

        groups = []
        group = []
        for i, line in enumerate(self.lines, 1):
            group.append(line)
            if i % 3 == 0:
                groups.append(group)
                group = []

        priorities_sum = 0
        for group in groups:
            intersection_chars = (
                set(group[0]).intersection(set(group[1])).intersection(set(group[2]))
            )
            for char in intersection_chars:
                char_priority = priorities.get(char)
                priorities_sum += char_priority
        return priorities_sum
