from advent_of_code.basesolver import BaseSolver


class Y2022D01Solver(BaseSolver):
    def solve_part_a(self):
        elf_sums = []
        for chunk in self.chunks(type=int):
            elf_sums.append(sum(chunk))
        return max(elf_sums)

    def solve_part_b(self):
        elf_sums = []
        for chunk in self.chunks(type=int):
            elf_sums.append(sum(chunk))
        elf_sums.sort(reverse=True)
        return elf_sums[0] + elf_sums[1] + elf_sums[2]
