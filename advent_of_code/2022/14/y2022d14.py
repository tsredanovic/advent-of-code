from advent_of_code.basesolver import BaseSolver

MAX_INT = 2**10000

class Sand:
    def __init__(self, start_point, rocks, floor_exists=False) -> None:
        self.start_point = start_point

        self.rocks = rocks
        self.rocks_points = {}
        for rock in rocks:
            for point in rock.points.values():
                self.rocks_points[point.pos] = point

        self.rocks_min_x = MAX_INT
        self.rocks_max_x = -MAX_INT
        self.rocks_min_y = MAX_INT
        self.rocks_max_y = -MAX_INT
        for point in self.rocks_points.values():
            if point.x < self.rocks_min_x:
                self.rocks_min_x = point.x
            if point.x > self.rocks_max_x:
                self.rocks_max_x = point.x
            if point.y < self.rocks_min_y:
                self.rocks_min_y = point.y
            if point.y > self.rocks_max_y:
                self.rocks_max_y = point.y
        
        self.floor_y = self.rocks_max_y + 2

        self.grains_points = {}

        self.floor_exists = floor_exists
    
    def drop_sand(self):
        while True:
            final_grain_point = self.drop_grain()
            if not final_grain_point:
                break
            self.grains_points[final_grain_point.pos] = final_grain_point
            if final_grain_point.pos == self.start_point.pos:
                break
            #self.print()

    def drop_grain(self):
        current_point = Point(self.start_point.x, self.start_point.y)
        #print(current_point)
        while True:
            possible_next_points = [
                Point(current_point.x, current_point.y + 1),
                Point(current_point.x - 1, current_point.y + 1),
                Point(current_point.x + 1, current_point.y + 1),
            ]
            next_point = None
            for possible_next_point in possible_next_points:
                is_rock_at_possible_next_point = True if self.rocks_points.get(possible_next_point.pos) else False
                is_grain_at_possible_next_point = True if self.grains_points.get(possible_next_point.pos) else False
                #print(possible_next_point, is_rock_at_possible_next_point)
                if not is_rock_at_possible_next_point and not is_grain_at_possible_next_point:
                    next_point = possible_next_point
                    break
            if not next_point:
                return current_point
            if next_point.y == self.floor_y:
                if not self.floor_exists:
                    return None
                else:
                    return current_point
            current_point = next_point
    
    def print(self):
        lines = []
        line = ""
        for y in range(self.start_point.y, self.floor_y + 1):
            for x in range(self.rocks_min_x, self.rocks_max_x + 1):
                pos = (x, y)
                char = '.'
                if self.grains_points.get(pos):
                    char = 'o'
                elif self.start_point.pos == pos:
                    char = '+'
                elif self.rocks_points.get(pos):
                    char = '#'
                elif y == self.floor_y:
                    char = '#'
                line += char
            lines.append(line)
            line = ""
        print("\n".join(lines))


class Rock:
    def __init__(self, points) -> None:
        self.points = points

    def rocks_from_lines(lines):
        rocks = []
        for line in lines:
            rocks.append(Rock.rock_from_line(line))
        return rocks
    
    def rock_from_line(line):
        rock_edges = [Point(int(point_str.split(',')[0]), int(point_str.split(',')[1])) for point_str in line.split(' -> ')]
        points = {}
        for i in range(1, len(rock_edges)):
            rock_edge_1 = rock_edges[i-1]
            rock_edge_2 = rock_edges[i]
            if rock_edge_1.x == rock_edge_2.x:
                min_y = min(rock_edge_1.y, rock_edge_2.y)
                max_y = max(rock_edge_1.y, rock_edge_2.y)
                for y in range(min_y, max_y + 1):
                    point = Point(rock_edge_1.x, y)
                    if point.pos not in points.keys():
                        points[point.pos] = point
            if rock_edge_1.y == rock_edge_2.y:
                min_x = min(rock_edge_1.x, rock_edge_2.x)
                max_x = max(rock_edge_1.x, rock_edge_2.x)
                for x in range(min_x, max_x + 1):
                    point = Point(x, rock_edge_1.y)
                    if point.pos not in points.keys():
                        points[point.pos] = point
        return Rock(points)

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @property
    def pos(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        return str(self.pos)

    def __repr__(self) -> str:
        return str(self)

class Y2022D14Solver(BaseSolver):
    def solve_part_a(self):
        start_point = Point(500, 0)
        rocks = Rock.rocks_from_lines(self.lines)
        sand = Sand(start_point, rocks)
        #sand.print()
        sand.drop_sand()
        return len(sand.grains_points)

    def solve_part_b(self):
        start_point = Point(500, 0)
        rocks = Rock.rocks_from_lines(self.lines)
        sand = Sand(start_point, rocks, floor_exists=True)
        #sand.print()
        sand.drop_sand()
        return len(sand.grains_points)
