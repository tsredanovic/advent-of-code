from basesolver import BaseSolver

class Elf:
    def __init__(self, range_str: str) -> None:
        self.values = [i for i in range(int(range_str.split('-')[0]), int(range_str.split('-')[1]) + 1)]
    
    def fully_contains(self, elf) -> bool:
        if set(self.values).intersection(elf.values) == set(self.values):
            return True
        return False
    
    def overlaps(self, elf) -> bool:
        if set(self.values).intersection(elf.values):
            return True
        return False


class Y2022D04Solver(BaseSolver):
    def solve_part_a(self):
        fully_contains_count = 0
        for line in self.lines:
            ranges = line.split(',')
            elf_1 = Elf(ranges[0])
            elf_2 = Elf(ranges[1])
            if elf_1.fully_contains(elf_2) or elf_2.fully_contains(elf_1):
                fully_contains_count += 1
        return fully_contains_count
    

    def solve_part_b(self):
        overlaps_count = 0
        for line in self.lines:
            ranges = line.split(',')
            elf_1 = Elf(ranges[0])
            elf_2 = Elf(ranges[1])
            if elf_1.overlaps(elf_2) or elf_2.overlaps(elf_1):
                overlaps_count += 1
        return overlaps_count
