class NotImplementedError(Exception):
    pass

class BaseSolver:
    def __init__(self, data, part):
        self.data = data

        self.part = part
    
    @property
    def lines(self):
        return self.data.splitlines()

    @property
    def numbers(self):
        return [int(n) for n in self.data.splitlines()]

    def solve_part_a(self):
        raise NotImplementedError('part a solution not implemented')
    
    def solve_part_b(self):
        raise NotImplementedError('part b solution not implemented')