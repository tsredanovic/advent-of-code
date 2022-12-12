from advent_of_code.basesolver import BaseSolver

class Point:
    def __init__(self, x, y, char) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.elevation = Point.elevation_from_char(self.char)

        self.visited = False
        self.distance = 0 if self.char == 'S' else 2**10000
        self.distance_from_point = None

    @property
    def pos(self):
        return (self.x, self.y)

    def elevation_from_char(char):
        if char == 'S':
            return 0
        elif char == 'E':
            return 27
        return ord(char) - 96 # a -> 1, z -> 26
    
    def is_start(self):
        return True if self.char == 'S' else False

    def is_end(self):
        return True if self.char == 'E' else False

    def __str__(self) -> str:
        return str('{} -> {}'.format(self.pos, self.char))

    def __repr__(self) -> str:
        return str(self)

class Map:
    def __init__(self, points, start_point, end_point) -> None:
        self.points = points
        self.start_point = start_point
        self.end_point = end_point
        self.w = max([point.x for point in self.points.values()]) + 1
        self.h = max([point.y for point in self.points.values()]) + 1
    
    def point_neighbors_positions(self, point):
        neighbors_positions = []
        if point.x > 0:
            neighbors_positions.append((point.x - 1, point.y))
        if point.x < self.w - 1:
            neighbors_positions.append((point.x + 1, point.y))
        if point.y > 0:
            neighbors_positions.append((point.x, point.y - 1))
        if point.y < self.h - 1:
            neighbors_positions.append((point.x, point.y + 1))
        return neighbors_positions
    
    def point_neighbors(self, point):
        neighbors = []
        for neighbor_pos in self.point_neighbors_positions(point):
            neighbors.append(self.points[neighbor_pos])
        return neighbors
    
    def point_unvisited_neighbors(self, point):
        neighbors = self.point_neighbors(point)
        unvisited_neighbors = [neighbor for neighbor in neighbors if not neighbor.visited]
        return unvisited_neighbors
    
    def point_possible_neighbors(self, point):
        unvisited_neighbors = self.point_unvisited_neighbors(point)
        possible_neighbors = [unvisited_neighbor for unvisited_neighbor in unvisited_neighbors if unvisited_neighbor.elevation <= point.elevation + 1]
        return possible_neighbors
    
    def get_unvisited_points(self):
        return [point for point in self.points.values() if not point.visited]

    def get_next_point(self):
        unvisited_points = self.get_unvisited_points()
        sorted_unvisited_points = sorted(unvisited_points, key=lambda point: point.distance)
        return sorted_unvisited_points[0]

    def turn_S_into_a(self):
        for point in self.points.values():
            if point.char == 'S':
                point.char = 'a'
                point.distance = 2**10000
                break


    def print(self):
        lines = []
        line = ""
        for y in range(self.h):
            for x in range(self.w):
                point = self.points[(x, y)]
                line += point.char
            lines.append(line)
            line = ""
        print("\n".join(lines))

    def map_from_lines(lines):
        points = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                point = Point(x, y, char)
                if point.is_start():
                    start_point = point
                elif point.is_end():
                    end_point = point
                points[point.pos] = point
        return Map(points, start_point, end_point)

class Y2022D12Solver(BaseSolver):
    def solve(self, map):
        current_point = map.start_point
        while True:
            #print('Current point: {}'.format(current_point))
            possible_neighbors = map.point_possible_neighbors(current_point)
            #print('  Possible neighbors: {}'.format(possible_neighbors))
            for possible_neighbor in possible_neighbors:
                distance = current_point.distance + 1
                possible_neighbor.distance = distance if distance < possible_neighbor.distance else possible_neighbor.distance
            current_point.visited = True
            if current_point.is_end():
                return current_point.distance
            current_point = map.get_next_point()

    def solve_part_a(self):
        map = Map.map_from_lines(self.lines)
        return self.solve(map)

    def solve_part_b(self):
        map = Map.map_from_lines(self.lines)
        map.turn_S_into_a()

        # find all a points
        a_points_positions = []
        for point in map.points.values():
            if point.char == 'a':
                a_points_positions.append(point.pos)
        
        a_points_count = len(a_points_positions)

        min_distance = 2**10000
        for i, a_point_position in enumerate(a_points_positions, 1):
            print('Solving {}/{}'.format(i, a_points_count))
            map = Map.map_from_lines(self.lines)
            map.turn_S_into_a()
            map.start_point = map.points[a_point_position]
            map.start_point.distance = 0
            distance = self.solve(map)
            if distance < min_distance:
                min_distance = distance

        return min_distance
