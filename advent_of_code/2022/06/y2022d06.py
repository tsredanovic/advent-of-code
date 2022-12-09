from advent_of_code.basesolver import BaseSolver


class Device:
    def __init__(self, stream) -> None:
        self.stream = stream

    def get_start_of_packet(self, marker_len):
        for i in range(len(self.stream) - marker_len - 1):
            possible_start_of_packet = self.stream[i : i + marker_len]
            if len(set(possible_start_of_packet)) == marker_len:
                return i
        return None


class Y2022D06Solver(BaseSolver):
    def solve(self, marker_len):
        stream = self.lines[0]
        device = Device(stream)
        return device.get_start_of_packet(marker_len=marker_len) + marker_len

    def solve_part_a(self):
        return self.solve(4)

    def solve_part_b(self):
        return self.solve(14)
