from basesolver import BaseSolver


def calc_points_diff(point_1, point_2):
    return point_1.x - point_2.x, point_1.y - point_2.y


def calc_points_touching(point_1, point_2):
    points_diff_x, points_diff_y = calc_points_diff(point_1, point_2)

    if abs(points_diff_x) <= 1 and abs(points_diff_y) <= 1:
        return True
    
    return False


class Point:
    def __init__(self, x, y, mark='-') -> None:
        self.x = x
        self.y = y
        self.mark = str(mark)
    
    @property
    def pos(self):
        return (self.x, self.y)
    
    def __str__(self) -> str:
        return str(self.pos)
    
    def __repr__(self) -> str:
        return str(self)


class Grid:
    def __init__(self, number_of_points) -> None:
        self.number_of_points = number_of_points
        self.start_point = Point(0, 0, 's')
        self.point_groups = {}
        for i in range(self.number_of_points):
            self.point_groups[i] = [Point(0, 0, str(i))]
    
    def calc_next_0_point(self, direction, current_point, i):
        if direction == 'R':
            next_point = Point(current_point.x + 1, current_point.y, i)
        elif direction == 'L':
            next_point = Point(current_point.x - 1, current_point.y, i)
        elif direction == 'U':
            next_point = Point(current_point.x, current_point.y + 1, i)
        elif direction == 'D':
            next_point = Point(current_point.x, current_point.y - 1, i)
        return next_point

    def calc_next_point(self, next_point, current_point, i):
        if calc_points_touching(next_point, current_point):
            return Point(current_point.x, current_point.y, i)
        else:
            points_diff_x, points_diff_y = calc_points_diff(next_point, current_point)

            if points_diff_x == 0: # On same column, must move y
                x_to_add = 0
                if points_diff_y == 2:
                    y_to_add = 1
                elif points_diff_y == -2:
                    y_to_add = -1
                else:
                    y_to_add = 0

            elif points_diff_y == 0: # On same row, must move x
                y_to_add = 0
                if points_diff_x == 2:
                    x_to_add = 1
                elif points_diff_x == -2:
                    x_to_add = -1
                else:
                    x_to_add = 0

            else:  # On diff row and column, must move diagonally
                x_to_add = 1 if points_diff_x >= 0 else -1
                y_to_add = 1 if points_diff_y >= 0 else -1
            return Point(current_point.x + x_to_add, current_point.y + y_to_add, i)

    def move(self, move_line):
        direction = move_line.split(' ')[0]
        step_count = int(move_line.split(' ')[1])

        for _ in range(step_count):
            for i in range(self.number_of_points):
                current_point = self.point_groups[i][-1]
                if i == 0:
                    next_point = self.calc_next_0_point(direction, current_point, i)
                else:
                    next_point = self.calc_next_point(self.point_groups[i-1][-1], current_point, i)

                self.point_groups[i].append(next_point)
    
    @property
    def w(self):
        return max([point.x for point in self.point_groups[0]]) + 1

    @property
    def h(self):
        return max([point.y for point in self.point_groups[0]]) + 1
    

    def print_points_at(self, i):
        line = ''
        for y in range(self.h):
            for x in range(self.w):
                pos = (x, y)

                point_at_pos = None

                if pos == self.start_point.pos:
                    point_at_pos = self.start_point

                for pg_i in range(self.number_of_points):
                    point_group = self.point_groups[pg_i]
                    point = point_group[i]
                    if pos == point.pos:
                        point_at_pos = point
                        break

                line += str(point_at_pos.mark) if point_at_pos else '.'

            print(line)
            line = ''

    def print(self):
        for i in range(len(self.point_groups[0])):
            self.print_points_at(i)
            print()


class Y2022D09Solver(BaseSolver):
    def solve(self, number_of_points):
        grid = Grid(number_of_points)
        for line in self.lines:
            grid.move(line)
        return len(set([point.pos for point in grid.point_groups[number_of_points - 1]]))

    def solve_part_a(self):
        NUMBER_OF_POINTS = 2
        return self.solve(NUMBER_OF_POINTS)
    

    def solve_part_b(self):
        NUMBER_OF_POINTS = 10
        return self.solve(NUMBER_OF_POINTS)
