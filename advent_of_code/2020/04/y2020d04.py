from advent_of_code.basesolver import BaseSolver


class PassportFactory:
    def extract_passports(lines):
        passports_lines = PassportFactory.separate_passport_lines(lines)
        passports = []
        for passport_lines in passports_lines:
            passport = PassportFactory.passport_from_lines(passport_lines)
            passports.append(passport)
        return passports

    def separate_passport_lines(lines):
        passports_lines = []
        single_passport_lines = []
        for line in lines:
            if line:
                single_passport_lines.append(line)
            else:
                passports_lines.append(single_passport_lines)
                single_passport_lines = []
        passports_lines.append(single_passport_lines)
        return passports_lines

    def passport_from_lines(lines):
        passport_dict = {}
        for line in lines:
            kvs = line.split(" ")
            for kv in kvs:
                key = kv.split(":")[0]
                value = kv.split(":")[1]
                passport_dict[key] = value
        return Passport(
            byr=passport_dict.get("byr"),
            iyr=passport_dict.get("iyr"),
            eyr=passport_dict.get("eyr"),
            hgt=passport_dict.get("hgt"),
            hcl=passport_dict.get("hcl"),
            ecl=passport_dict.get("ecl"),
            pid=passport_dict.get("pid"),
            cid=passport_dict.get("cid"),
        )


class Passport:
    """
    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)
    """

    def __init__(self, byr, iyr, eyr, hgt, hcl, ecl, pid, cid):
        self.byr = byr
        self.iyr = iyr
        self.eyr = eyr
        self.hgt = hgt
        self.hcl = hcl
        self.ecl = ecl
        self.pid = pid
        self.cid = cid

    def __str__(self):
        string = ""
        for key, value in self.__dict__.items():
            string += "{} = {}\n".format(key, value)
        return string

    def __repr__(self):
        return self.__str__()

    def is_valid_1(self):
        required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        for req_field_name in required_fields:
            if not getattr(self, req_field_name, None):
                return False
        return True

    def is_valid_2(self):
        if not self.is_valid_1():
            return False

        if not self.is_byr_valid(getattr(self, "byr", None)):
            return False

        if not self.is_iyr_valid(getattr(self, "iyr", None)):
            return False

        if not self.is_eyr_valid(getattr(self, "eyr", None)):
            return False

        if not self.is_hgt_valid(getattr(self, "hgt", None)):
            return False

        if not self.is_hcl_valid(getattr(self, "hcl", None)):
            return False

        if not self.is_ecl_valid(getattr(self, "ecl", None)):
            return False

        if not self.is_pid_valid(getattr(self, "pid", None)):
            return False

        return True

    def check_len(self, string, length):
        if len(string) != length:
            return False
        return True

    def check_if_in_range(self, string, valid_range):
        integer = int(string)
        if valid_range[0] <= integer <= valid_range[1]:
            return True
        else:
            return False

    def check_if_only_chars_in_string(self, string, valid_chars):
        for char in string:
            if char not in valid_chars:
                return False
        return True

    def check_if_string_one_of(self, string, valid_values):
        if string in valid_values:
            return True
        else:
            return False

    def is_byr_valid(self, byr):
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        if not self.check_len(byr, 4):
            return False
        if not self.check_if_in_range(byr, (1920, 2002)):
            return False
        return True

    def is_iyr_valid(self, iyr):
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        if not self.check_len(iyr, 4):
            return False
        if not self.check_if_in_range(iyr, (2010, 2020)):
            return False
        return True

    def is_eyr_valid(self, eyr):
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        if not self.check_len(eyr, 4):
            return False
        if not self.check_if_in_range(eyr, (2020, 2030)):
            return False
        return True

    def is_hgt_valid(self, hgt):
        # hgt (Height) - a number followed by either cm or in:
        # If cm, the number must be at least 150 and at most 193.
        # If in, the number must be at least 59 and at most 76.
        measure = None
        if hgt.endswith("cm"):
            measure = "cm"
        elif hgt.endswith("in"):
            measure = "in"
        if not measure:
            return False

        value = hgt.rstrip("cm").rstrip("in")
        if measure == "cm" and not self.check_if_in_range(value, (150, 193)):
            return False
        if measure == "in" and not self.check_if_in_range(value, (59, 76)):
            return False

        return True

    def is_hcl_valid(self, hcl):
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        if hcl[0] != "#":
            return False

        value = hcl.lstrip("#")
        if not self.check_len(value, 6):
            return False

        valid_chars = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
        ]

        if not self.check_if_only_chars_in_string(value, valid_chars):
            return False

        return True

    def is_ecl_valid(self, ecl):
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        valid_values = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        if not self.check_if_string_one_of(ecl, valid_values):
            return False
        return True

    def is_pid_valid(self, pid):
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        if not self.check_len(pid, 9):
            return False

        if not pid.isdigit():
            return False

        return True


class Y2020D04Solver(BaseSolver):
    def solve_part_a(self):
        passports = PassportFactory.extract_passports(self.lines)

        valid_pp_count = 0
        for pp in passports:
            if pp.is_valid_1():
                valid_pp_count += 1

        return str(valid_pp_count)

    def solve_part_b(self):
        passports = PassportFactory.extract_passports(self.lines)

        valid_pp_count = 0
        for pp in passports:
            if pp.is_valid_2():
                valid_pp_count += 1

        return str(valid_pp_count)
