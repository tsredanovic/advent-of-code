from basesolver import BaseSolver


def calculate_output(input_list, pos_1_value, pos_2_value):
    input_list[1] = pos_1_value
    input_list[2] = pos_2_value

    current_possition = 0
    while True:
        if current_possition > len(input_list):
            break

        current_value = input_list[current_possition]

        if current_value == 99:
            break
        else:
            first_param = input_list[current_possition + 1]
            second_param = input_list[current_possition + 2]
            third_param = input_list[current_possition + 3]

            first_number = input_list[first_param]
            second_number = input_list[second_param]

            if current_value == 1:
                result = first_number + second_number
            else:
                result = first_number * second_number

            input_list[third_param] = result

        current_possition += 4

    return input_list[0]


class Y2019D02Solver(BaseSolver):
    def solve_part_a(self):
        input_list = [int(x.strip()) for x in self.data.split(',')]
        return calculate_output(input_list, 12, 2)
    

    def solve_part_b(self):
        desired_output = 19690720

        for noun in range(0, 100):
            for verb in range(0, 100):
                input_list = [int(x.strip()) for x in self.data.split(',')]

                output = calculate_output(input_list, noun, verb)

                if output == desired_output:
                    return 100 * noun + verb


