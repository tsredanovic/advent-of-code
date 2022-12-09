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
        map_str = ''
        for y in range(self.height):
            for x in range(self.width):
                map_str += self.position_values[(y, x)]
            map_str += '\n'
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
        possible_neighbour_positions = [(x, y1), (x, y2), (x1, y), (x2, y)]

        neighbour_positions = []
        for possible_neighbour_position in possible_neighbour_positions:
            if self.position_values.get(possible_neighbour_position) is not None:
                neighbour_positions.append(possible_neighbour_position)

        return neighbour_positions
    
    def get_neighbour_values(self, position):
        neighbour_positions = self.get_neighbour_positions(position)
        neighbour_values = []
        for neighbour_position in neighbour_positions:
            neighbour_value = self.position_values.get(neighbour_position)
            if neighbour_value is not None:
                neighbour_values.append(neighbour_value)
        
        return neighbour_values
    
    def is_low_point(self, position):
        value = self.position_values[position]
        neighbour_values = self.get_neighbour_values(position)
        for neighbour_value in neighbour_values:
            if value >= neighbour_value:
                return False
        return True
    
    def get_low_points(self):
        low_points = []
        for y in range(self.height):
            for x in range(self.width):
                position = (y, x)
                if self.is_low_point(position):
                    low_points.append(position)
        return low_points
    
    def get_low_point_values(self):
        low_point_values = []
        for low_point in self.get_low_points():
            low_point_values.append(self.position_values[low_point])
        return low_point_values
    
    def get_low_point_risk_level(self, position):
        return self.position_values[position] + 1
    
    def get_total_low_points_risk_level(self):
        low_points = self.get_low_points()
        total_low_points_risk_level = 0
        for low_point in low_points:
            total_low_points_risk_level += self.get_low_point_risk_level(low_point)
        return total_low_points_risk_level
    
    def get_basin_positions(self, position):
        basin_positions = []
        current_positions = [position]
        while current_positions:
            current_position = current_positions.pop()
            if current_position not in basin_positions:
                basin_positions.append(current_position)
            neighbour_positions = self.get_neighbour_positions(current_position)
            for neighbour_position in neighbour_positions:
                if self.position_values[neighbour_position] != 9 and neighbour_position not in basin_positions:
                    current_positions.append(neighbour_position)
        return basin_positions

    def get_basin_values(self, position):
        basin_positions = self.get_basin_positions(position)
        basin_values = []
        for basin_position in basin_positions:
            basin_values.append(self.position_values[basin_position])
        return basin_values
    
    def get_basin_size(self, position):
        return len(self.get_basin_positions(position))

class Y2021D09Solver(BaseSolver):
    def solve_part_a(self):
        map = Map(self.lines)
        return map.get_total_low_points_risk_level()
    

    def solve_part_b(self):
        map = Map(self.lines)
        low_points = map.get_low_points()
        basin_sizes = []
        for low_point in low_points:
            basin_sizes.append(map.get_basin_size(low_point))
        three_largest_basin_sizes = sorted(basin_sizes, reverse=True)[:3]
        result = 1
        for size in three_largest_basin_sizes:
            result *= size
        return result
