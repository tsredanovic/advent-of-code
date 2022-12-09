from advent_of_code.basesolver import BaseSolver


class Map:
    def __init__(self, lines) -> None:
        self.height = len(lines)
        self.width = len(lines[0])
        self.position_values = {}
        for y in range(self.height):
            for x in range(self.width):
                self.position_values[(y, x)] = int(lines[y][x])

    def __str__(self) -> str:
        map_str = ""
        for y in range(self.height):
            for x in range(self.width):
                map_str += str(self.position_values[(y, x)])
            map_str += "\n"
        return map_str

    def __repr__(self) -> str:
        return str(self)

    def get_neighbour_positions(self, position):
        x = position[0]
        y = position[1]
        x1 = x - 1
        x2 = x + 1
        y1 = y - 1
        y2 = y + 1
        possible_neighbour_positions = [
            (x, y1),
            (x, y2),
            (x1, y),
            (x2, y),
            (x1, y1),
            (x1, y2),
            (x2, y1),
            (x2, y2),
        ]

        neighbour_positions = []
        for possible_neighbour_position in possible_neighbour_positions:
            if self.position_values.get(possible_neighbour_position) is not None:
                neighbour_positions.append(possible_neighbour_position)

        return neighbour_positions

    def increase_values(self):
        for y in range(self.height):
            for x in range(self.width):
                self.position_values[(y, x)] += 1

    def get_flashable_positions(self):
        flashable_positions = []
        for y in range(self.height):
            for x in range(self.width):
                position = (y, x)
                if self.position_values[position] > 9:
                    flashable_positions.append(position)
        return flashable_positions

    def execute_flash(self, position):
        neighbour_positions = self.get_neighbour_positions(position)
        for neighbour_position in neighbour_positions:
            self.position_values[neighbour_position] += 1

    def reset_positions(self, flashed_positions):
        for position in flashed_positions:
            self.position_values[position] = 0

    def execute_step(self):
        self.increase_values()
        flashed_this_step_positions = []
        while True:
            flashable_positions = self.get_flashable_positions()
            flashable_positions = [
                flashable_position
                for flashable_position in flashable_positions
                if flashable_position not in flashed_this_step_positions
            ]
            if not flashable_positions:
                break
            for flashable_position in flashable_positions:
                self.execute_flash(flashable_position)
                flashed_this_step_positions.append(flashable_position)
        self.reset_positions(flashed_this_step_positions)
        return len(flashed_this_step_positions)


class Y2021D11Solver(BaseSolver):
    def solve_part_a(self):
        map = Map(self.lines)
        steps = 100

        print("Initial:")
        print(map)
        total_flash_count = 0
        for i in range(1, steps + 1):
            step_flash_count = map.execute_step()
            total_flash_count += step_flash_count
            print("After step {}:".format(i))
            print(map)
        return total_flash_count

    def solve_part_b(self):
        map = Map(self.lines)
        map_size = map.width * map.height
        step = 0
        while True:
            step_flash_count = map.execute_step()
            step += 1
            if step_flash_count == map_size:
                return step
