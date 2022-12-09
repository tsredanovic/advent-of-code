
from advent_of_code.basesolver import BaseSolver


class Policy:
    def __init__(self, char, value1, value2):
        self.char = char
        self.value1 = int(value1)
        self.value2 = int(value2)
    
    def __str__(self):
        return '{}-{} {}'.format(
            self.value1,
            self.value2,
            self.char
        )
    
    def __repr__(self):
        return self.__str__()


class Y2020D02Solver(BaseSolver):
    def extract_policy(self, line):
        policy_part = line.split(':')[0]
        char = policy_part.split(' ')[1]
        value1 = policy_part.split(' ')[0].split('-')[0]
        value2 = policy_part.split(' ')[0].split('-')[1]
        return Policy(char, value1, value2)
    
    def extract_password(self, line):
        return line.split(':')[1].strip()
    
    def check_password_validity_1(self, password, policy):
        chars_in_pass = password.count(policy.char)
        if policy.value1 <= chars_in_pass <= policy.value2:
            return True
        else:
            return False
    
    def check_password_validity_2(self, password, policy):
        char_at_poss_1 = password[policy.value1 - 1]
        char_at_poss_2 = password[policy.value2 - 1]
        if (char_at_poss_1 == policy.char and char_at_poss_2 == policy.char) or (char_at_poss_1 != policy.char and char_at_poss_2 != policy.char):
            return False
        else:
            return True

    def solve_part_a(self):
        valid_passwords_count = 0
        for line in self.lines:
            policy = self.extract_policy(line)
            password = self.extract_password(line)
            if self.check_password_validity_1(password, policy):
                valid_passwords_count += 1

        return str(valid_passwords_count)
    

    def solve_part_b(self):
        valid_passwords_count = 0
        for line in self.lines:
            policy = self.extract_policy(line)
            password = self.extract_password(line)
            if self.check_password_validity_2(password, policy):
                valid_passwords_count += 1

        return str(valid_passwords_count)

