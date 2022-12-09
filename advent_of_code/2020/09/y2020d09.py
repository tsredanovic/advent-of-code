import itertools

from advent_of_code.basesolver import BaseSolver


class XMAS:
    def __init__(self, numbers, preamble_length):
        self.numbers = numbers
        self.preamble_length = preamble_length

    def read_previous_numbers(self, position):
        start_index = position - self.preamble_length
        end_index = position
        return self.numbers[start_index:end_index]

    def check_validity(self, number, numbers):
        for pair in itertools.product(numbers, repeat=2):
            num1 = pair[0]
            num2 = pair[1]
            if num1 == num2:
                continue
            if num1 + num2 == number:
                return True
        return False

    def find_invalid_number(self):
        position = self.preamble_length
        while True:
            if position >= len(self.numbers):
                return None

            number = self.numbers[position]
            previous_numbers = self.read_previous_numbers(position)
            if not self.check_validity(number, previous_numbers):
                return number

            position += 1

    def find_cont_nums_that_sum_to_num(self, number):
        starting_positions = range(0, len(self.numbers))
        for starting_pos in starting_positions:
            # print('Start: {}'.format(starting_pos))
            offset = 0
            current_sum = 0
            nums = []
            while current_sum < number:
                current_num = self.numbers[starting_pos + offset]
                nums.append(current_num)
                # print(nums)
                current_sum += current_num

                if current_sum == number and len(nums) >= 2:
                    return nums

                offset += 1


class Y2020D09Solver(BaseSolver):
    def solve_part_a(self):
        PREAMBLE_LENGTH = 25
        xmas = XMAS(self.numbers, PREAMBLE_LENGTH)
        invalid_number = xmas.find_invalid_number()
        return str(invalid_number)

    def solve_part_b(self):
        PREAMBLE_LENGTH = 25
        xmas = XMAS(self.numbers, PREAMBLE_LENGTH)
        invalid_number = xmas.find_invalid_number()
        # print('Checking {}'.format(invalid_number))
        cont_nums_that_sum_to_num = xmas.find_cont_nums_that_sum_to_num(invalid_number)
        result = min(cont_nums_that_sum_to_num) + max(cont_nums_that_sum_to_num)
        return str(result)
