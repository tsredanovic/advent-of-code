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

    def chunks(self, delimiter="", type=str):
        chunks = []
        chunk = []
        for line in self.lines:
            if line != delimiter:
                chunk.append(type(line))
            else:
                chunks.append(chunk)
                chunk = []
        if chunk:
            chunks.append(chunk)
        return chunks

    def solve_part_a(self):
        raise NotImplementedError("part a solution not implemented")

    def solve_part_b(self):
        raise NotImplementedError("part b solution not implemented")
