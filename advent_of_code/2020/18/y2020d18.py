from advent_of_code.basesolver import BaseSolver


def closest_left_index_of(string, char, search_i):
    while True:
        search_i -= 1
        if string[search_i] == char:
            return search_i


def evaluate(string):
    args = string.split(" ")
    first = int(args.pop(0))
    while args:
        operator = args.pop(0)
        second = int(args.pop(0))
        if operator == "*":
            first *= second
        elif operator == "+":
            first += second
    return first


def advanced_evaluate(string):
    current_args = string.split(" ")
    while "+" in current_args:
        plus_index = current_args.index("+")
        first = int(current_args[plus_index - 1])
        second = int(current_args[plus_index + 1])
        fs_sum = first + second
        current_args[plus_index] = fs_sum
        current_args.pop(plus_index + 1)
        current_args.pop(plus_index - 1)

    result = 1
    for arg in current_args:
        if arg != "*":
            result *= int(arg)
    return result


def solve(lines, advanced=False):
    sum_of_line_results = 0
    for line in lines:
        current_eq = line
        while True:
            if ")" not in current_eq:
                if not advanced:
                    line_result = evaluate(current_eq)
                else:
                    line_result = advanced_evaluate(current_eq)
                # print(line_result)
                break

            close_index = current_eq.index(")")
            open_index = closest_left_index_of(current_eq, "(", close_index)
            part = current_eq[open_index + 1 : close_index]
            if not advanced:
                part_result = evaluate(part)
            else:
                part_result = advanced_evaluate(part)

            current_eq = (
                current_eq[:open_index]
                + str(part_result)
                + current_eq[close_index + 1 :]
            )

        sum_of_line_results += line_result

    return sum_of_line_results


class Y2020D18Solver(BaseSolver):
    def solve_part_a(self):
        result = solve(self.lines)
        return str(result)

    def solve_part_b(self):
        result = solve(self.lines, advanced=True)
        return str(result)
