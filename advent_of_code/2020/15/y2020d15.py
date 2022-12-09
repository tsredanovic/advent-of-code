from advent_of_code.basesolver import BaseSolver


def solve(starting_nums, final_i):
    last_num_spoken = starting_nums[-1]
    spoken_at = {}

    for i in range(0, len(starting_nums) - 1):
        number_spoken = starting_nums[i]
        spoken_at[number_spoken] = i

    last_num_spoken = starting_nums[-1]

    for i in range(len(starting_nums), final_i):
        step = i + 1
        if step % 10000 == 0:
            print("Step: {}/{}".format(step // 10000, final_i // 10000))
        elif step == final_i:
            print("Step: {}/{}".format(step, final_i))

        if last_num_spoken not in spoken_at.keys():
            number_spoken = 0
        else:
            number_spoken = i - spoken_at[last_num_spoken] - 1

        spoken_at[last_num_spoken] = i - 1

        last_num_spoken = number_spoken

    return last_num_spoken


class Y2020D15Solver(BaseSolver):
    def solve_part_a(self):
        starting_nums = [int(value) for value in self.lines[0].split(",")]
        result = solve(starting_nums, 2020)
        return str(result)

    def solve_part_b(self):
        starting_nums = [int(value) for value in self.lines[0].split(",")]
        result = solve(starting_nums, 30000000)
        return str(result)
