import math

from advent_of_code.basesolver import BaseSolver

pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

char_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

char_ac_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

CORRUPTED = 'CORRUPTED'
INCOMPLETE = 'INCOMPLETE'

def parse_line(line):
    #print('Parsing line: {}'.format(line))
    expected_closes = []
    for char in line:
        if char in pairs.keys():
            expected_closes.append(pairs[char])
        else:
            expected_close = expected_closes.pop()
            if char != expected_close:
                #print('CORRUPTED - Expected {}, but found {} instead'.format(expected_close, char))
                return CORRUPTED, {'illegal_char': char}
    #print('INCOMPLETE')
    return INCOMPLETE, {'expected_closes': expected_closes}


class Y2021D10Solver(BaseSolver):
    def solve_part_a(self):
        points = 0
        for line in self.lines:
            line_result, data = parse_line(line)
            if line_result == CORRUPTED:
                points += char_points[data['illegal_char']]
        return points

    def solve_part_b(self):
        all_line_points = []
        for line in self.lines:
            line_result, data = parse_line(line)
            if line_result == INCOMPLETE:
                line_points = 0
                expected_closes = data['expected_closes']
                while expected_closes:
                    expected_close = expected_closes.pop()
                    line_points *= 5
                    line_points += char_ac_points[expected_close]
                all_line_points.append(line_points)
        return sorted(all_line_points)[math.floor(len(all_line_points)/2)]
