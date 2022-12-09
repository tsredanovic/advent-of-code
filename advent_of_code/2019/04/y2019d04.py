from advent_of_code.basesolver import BaseSolver


class Password:
    def __init__(self, num):
        self.num = num

    def check_rule_1(self):
        """
        It is a six-digit number.
        """
        if len(str(self.num)) == 6:
            return True
        return False

    def check_rule_2(self):
        """
        Two adjacent digits are the same (like 22 in 122345).
        """
        str_num = str(self.num)
        for i in range(len(str_num)):
            if i + 1 == len(str_num):
                break
            current_digit = str_num[i]
            next_digit = str_num[i + 1]
            if current_digit == next_digit:
                return True
        return False

    def check_rule_3(self):
        """
        Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
        """
        str_num = str(self.num)
        for i in range(len(str_num)):
            current_digit = int(str_num[i])
            right_of_current_digits = [int(digit) for digit in str_num[i + 1 :]]

            for rocd in right_of_current_digits:
                if rocd < current_digit:
                    return False
        return True

    def check_rule_4(self):
        """
        Two adjacent digits are the same (like 22 in 122345),
        but are not part of a larger group of matching digits (123444 no longer meets the criteria).
        """
        str_num = str(self.num)
        isolated_same_double_digits = 0
        for i in range(len(str_num)):
            if i + 1 == len(str_num):
                break
            current_digit = str_num[i]
            next_digit = str_num[i + 1]
            if current_digit == next_digit:
                left_border_index = i - 1
                right_border_index = i + 2
                left_border_digit = (
                    str_num[left_border_index] if left_border_index >= 0 else None
                )
                right_border_digit = (
                    str_num[right_border_index]
                    if right_border_index < len(str_num)
                    else None
                )
                if (
                    current_digit == left_border_digit
                    or current_digit == right_border_digit
                ):
                    continue
                isolated_same_double_digits += 1

        if isolated_same_double_digits:
            return True

        return False

    def is_valid_part_1(self):
        if self.check_rule_1() and self.check_rule_2() and self.check_rule_3():
            return True
        return False

    def is_valid_part_2(self):
        if self.check_rule_1() and self.check_rule_3() and self.check_rule_4():
            return True
        return False


def load_input(data):
    content = data.strip()
    return [int(num) for num in content.split("-")]


class Y2019D04Solver(BaseSolver):
    def solve_part_a(self):
        start, end = load_input(self.data)

        possible_pwd_cnt = 0
        for num in range(start, end + 1):
            if Password(num).is_valid_part_1():
                possible_pwd_cnt += 1

        return possible_pwd_cnt

    def solve_part_b(self):
        start, end = load_input(self.data)

        possible_pwd_cnt = 0
        for num in range(start, end + 1):
            if Password(num).is_valid_part_2():
                possible_pwd_cnt += 1

        return possible_pwd_cnt
