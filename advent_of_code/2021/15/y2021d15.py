from solvers.y2021d11 import Map

from advent_of_code.basesolver import BaseSolver


class Cavern(Map):
    def get_neighbour_positions(self, position):
        x = position[0]
        y = position[1]
        x1 = x - 1
        x2 = x + 1
        y1 = y - 1
        y2 = y + 1
        possible_neighbour_positions = [(x, y1), (x, y2), (x1, y), (x2, y)]

        neighbour_positions = []
        for possible_neighbour_position in possible_neighbour_positions:
            if self.position_values.get(possible_neighbour_position) is not None:
                neighbour_positions.append(possible_neighbour_position)

        return neighbour_positions

    def get_not_visited_neighbour_positions(self, position, visited_positions):
        neighbour_positions = self.get_neighbour_positions(position)
        not_visited_neighbour_positions = []
        for neighbour_position in neighbour_positions:
            if neighbour_position not in visited_positions:
                not_visited_neighbour_positions.append(neighbour_position)
        return not_visited_neighbour_positions

    @property
    def end_position(self):
        return (self.height - 1, self.width - 1)


def get_shortest_path_index(paths):
    shortest_path_index = 0
    for i, path in enumerate(paths):
        if path["len"] < paths[shortest_path_index]["len"]:
            shortest_path_index = i

    return shortest_path_index


def too_slow(lines):
    cavern = Cavern(lines)

    paths = [{"positions": [(0, 0)], "len": cavern.position_values[(0, 0)]}]

    closest_pos_sum = 0
    while True:
        shortest_path_index = get_shortest_path_index(paths)
        shortest_path = paths.pop(shortest_path_index)
        last_position = shortest_path["positions"][-1]
        if last_position[0] + last_position[1] > closest_pos_sum:
            print(
                "{} -> {} | Paths: {}".format(
                    last_position, cavern.end_position, len(paths)
                )
            )
            closest_pos_sum = last_position[0] + last_position[1]
        if last_position == cavern.end_position:
            return shortest_path["len"] - cavern.position_values[(0, 0)]
        not_visited_neighbour_positions = cavern.get_not_visited_neighbour_positions(
            last_position, shortest_path["positions"]
        )
        for not_visited_neighbour_position in not_visited_neighbour_positions:
            paths.append(
                {
                    "positions": shortest_path["positions"]
                    + [not_visited_neighbour_position],
                    "len": shortest_path["len"]
                    + cavern.position_values[not_visited_neighbour_position],
                }
            )


def still_too_slow(lines):
    cavern = Cavern(lines)

    paths = {cavern.position_values[(0, 0)]: [[(0, 0)]]}

    closest_pos_sum = 0
    while True:
        shortest_len = min(list(paths.keys()))
        shortest_path = paths[shortest_len].pop()
        if not paths[shortest_len]:
            paths.pop(shortest_len)
        last_position = shortest_path[-1]
        if last_position[0] + last_position[1] > closest_pos_sum:
            print(
                "{} -> {} | Paths: {}".format(
                    last_position, cavern.end_position, len(paths)
                )
            )
            closest_pos_sum = last_position[0] + last_position[1]
        if last_position == cavern.end_position:
            return shortest_len - cavern.position_values[(0, 0)]
        not_visited_neighbour_positions = cavern.get_not_visited_neighbour_positions(
            last_position, shortest_path
        )
        for not_visited_neighbour_position in not_visited_neighbour_positions:
            new_path_len = (
                shortest_len + cavern.position_values[not_visited_neighbour_position]
            )
            if new_path_len not in paths.keys():
                paths[new_path_len] = [shortest_path + [not_visited_neighbour_position]]
            else:
                paths[new_path_len].append(
                    shortest_path + [not_visited_neighbour_position]
                )


class Y2021D15Solver(BaseSolver):
    def solve_part_a(self):
        return still_too_slow(self.lines)

    def solve_part_b(self):
        return None
