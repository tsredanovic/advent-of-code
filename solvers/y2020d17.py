from basesolver import BaseSolver

ACTIVE = '#'
INACTIVE = '.'

######
# 3D #
######

def active_points_from_lines(lines):
    active_points = []
    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            if lines[y][x] == ACTIVE:
                active_points.append(Point(x, y, 0))
    return active_points


def inactive_points_from_active_points(active_points):
    active_points_coords = [point.coords for point in active_points]
    min_x = min(point.x for point in active_points)
    max_x = max(point.x for point in active_points)
    min_y = min(point.y for point in active_points)
    max_y = max(point.y for point in active_points)
    min_z = min(point.z for point in active_points)
    max_z = max(point.z for point in active_points)

    inactive_points = []
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                if (x, y, z) not in active_points_coords:
                    inactive_points.append(Point(x, y, z))

    return inactive_points


def draw_all(points):
    # X, Y, Z
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)
    min_z = min(point.z for point in points)
    max_z = max(point.z for point in points)
    for z in range(min_z, max_z + 1):
        print('z={}'.format(z))
        draw_at_z(points, z, min_x, max_x, min_y, max_y)


def draw_at_z(points, z, min_x=None, max_x=None, min_y=None, max_y=None):
    # X and Y
    min_x = min_x if min_x else min(point.x for point in points)
    max_x = max_x if max_x else max(point.x for point in points)
    x_offset = 0 - min_x
    min_y = min_y if min_y else min(point.y for point in points)
    max_y = max_y if max_y else max(point.y for point in points)
    y_offset = 0 - min_y

    # Draw inactive map
    map_lines = []
    for y in range(max_y + y_offset + 1):
        map_line = []
        for x in range(max_x + x_offset + 1):
            map_line.append(INACTIVE)
        map_lines.append(map_line)
    
    # Draw points
    for point in points:
        if point.z == z:
            map_lines[point.y + y_offset][point.x + x_offset] = ACTIVE
    
    # Draw map
    for map_line in map_lines:
        print(''.join(map_line))


def count_active_points_at_coords(points, coords):
    points_coords = [point.coords for point in points]
    return len(set(points_coords) & set(coords))


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def coords(self):
        return (self.x, self.y, self.z)
    
    @property
    def neighbours_coords(self):
        neighbour_coords = []
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                for z in range(self.z-1, self.z+2):
                    if x == self.x and y == self.y and z == self.z:
                        continue
                    neighbour_coords.append((x, y, z))
        return neighbour_coords

######
# 4D #
######

def active_points_from_lines_4d(lines):
    active_points = []
    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            if lines[y][x] == ACTIVE:
                active_points.append(Point4D(x, y, 0 , 0))
    return active_points


def inactive_points_from_active_points_4d(active_points):
    active_points_coords = [point.coords for point in active_points]
    min_x = min(point.x for point in active_points)
    max_x = max(point.x for point in active_points)
    min_y = min(point.y for point in active_points)
    max_y = max(point.y for point in active_points)
    min_z = min(point.z for point in active_points)
    max_z = max(point.z for point in active_points)
    min_w = min(point.w for point in active_points)
    max_w = max(point.w for point in active_points)

    inactive_points = []
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                for w in range(min_w-1, max_w+2):
                    if (x, y, z, w) not in active_points_coords:
                        inactive_points.append(Point4D(x, y, z, w))

    return inactive_points


def draw_all_4d(points):
    # X, Y, Z, W
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)
    min_z = min(point.z for point in points)
    max_z = max(point.z for point in points)
    min_w = min(point.w for point in points)
    max_w = max(point.w for point in points)
    for w in range(min_w, max_w + 1):
        for z in range(min_z, max_z + 1):
            print('z={}, w={}'.format(z, w))
            draw_at_z_w(points, z, w, min_x, max_x, min_y, max_y)


def draw_at_z_w(points, z, w, min_x=None, max_x=None, min_y=None, max_y=None):
    # X and Y
    min_x = min_x if min_x else min(point.x for point in points)
    max_x = max_x if max_x else max(point.x for point in points)
    x_offset = 0 - min_x
    min_y = min_y if min_y else min(point.y for point in points)
    max_y = max_y if max_y else max(point.y for point in points)
    y_offset = 0 - min_y

    # Draw inactive map
    map_lines = []
    for y in range(max_y + y_offset + 1):
        map_line = []
        for x in range(max_x + x_offset + 1):
            map_line.append(INACTIVE)
        map_lines.append(map_line)
    
    # Draw points
    for point in points:
        if point.z == z and point.w == w:
            map_lines[point.y + y_offset][point.x + x_offset] = ACTIVE
    
    # Draw map
    for map_line in map_lines:
        print(''.join(map_line))


class Point4D:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    def __str__(self):
        return '({}, {}, {}, {})'.format(self.x, self.y, self.z, self.w)
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def coords(self):
        return (self.x, self.y, self.z, self.w)
    
    @property
    def neighbours_coords(self):
        neighbour_coords = []
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                for z in range(self.z-1, self.z+2):
                    for w in range(self.w-1, self.w+2):
                        if x == self.x and y == self.y and z == self.z and w == self.w:
                            continue
                        neighbour_coords.append((x, y, z, w))
        return neighbour_coords


class Y2020D17Solver(BaseSolver):
    def solve_part_a(self):
        active_points = active_points_from_lines(self.lines)
        inactive_points = inactive_points_from_active_points(active_points)

        cycle = 0
        while True:
            print('Cycle: {}'.format(cycle))
            if cycle == 6:
                return str(len(active_points))
            #draw_all(active_points)

            next_active_points = []

            # Go over active points
            for point in active_points:
                neighbours_coords = point.neighbours_coords
                active_neighbours_count = count_active_points_at_coords(active_points, neighbours_coords)
                if active_neighbours_count in [2, 3]:
                    next_active_points.append(point)
            
            # Go over inactive points
            for point in inactive_points:
                neighbours_coords = point.neighbours_coords
                active_neighbours_count = count_active_points_at_coords(active_points, neighbours_coords)
                if active_neighbours_count == 3:
                    next_active_points.append(point)
            
            active_points = next_active_points
            inactive_points = inactive_points_from_active_points(active_points)

            cycle += 1
    

    def solve_part_b(self):
        active_points = active_points_from_lines_4d(self.lines)
        inactive_points = inactive_points_from_active_points_4d(active_points)

        cycle = 0
        while True:
            print('Cycle: {}'.format(cycle))
            if cycle == 6:
                return str(len(active_points))
            #draw_all_4d(active_points)

            next_active_points = []

            # Go over active points
            for point in active_points:
                neighbours_coords = point.neighbours_coords
                active_neighbours_count = count_active_points_at_coords(active_points, neighbours_coords)
                if active_neighbours_count in [2, 3]:
                    next_active_points.append(point)
            
            # Go over inactive points
            for point in inactive_points:
                neighbours_coords = point.neighbours_coords
                active_neighbours_count = count_active_points_at_coords(active_points, neighbours_coords)
                if active_neighbours_count == 3:
                    next_active_points.append(point)
            
            active_points = next_active_points
            inactive_points = inactive_points_from_active_points_4d(active_points)

            cycle += 1


