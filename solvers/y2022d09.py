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
        self.mark = mark
    
    @property
    def pos(self):
        return (self.x, self.y)
    
    def __str__(self) -> str:
        return str(self.pos)
    
    def __repr__(self) -> str:
        return str(self)


class Grid:
    def __init__(self) -> None:
        self.start_point = Point(0, 0, 's')

        self.head_points = [Point(0, 0, 'H')]

        self.tail_points = [Point(0, 0, 'T')]

    def move(self, move_line):
        direction = move_line.split(' ')[0]
        step_count = int(move_line.split(' ')[1])

        for _ in range(step_count):
            current_head_point = self.head_points[-1]
            if direction == 'R':
                next_head_point = Point(current_head_point.x + 1, current_head_point.y, 'H')
            elif direction == 'L':
                next_head_point = Point(current_head_point.x - 1, current_head_point.y, 'H')
            elif direction == 'U':
                next_head_point = Point(current_head_point.x, current_head_point.y + 1, 'H')
            elif direction == 'D':
                next_head_point = Point(current_head_point.x, current_head_point.y - 1, 'H')

            current_tail_point = self.tail_points[-1]
            if calc_points_touching(next_head_point, current_tail_point):
                next_tail_point = Point(current_tail_point.x, current_tail_point.y, 'T')
            else:
                points_diff_x, points_diff_y = calc_points_diff(next_head_point, current_tail_point)

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
                next_tail_point = Point(current_tail_point.x + x_to_add, current_tail_point.y + y_to_add, 'T')

            self.head_points.append(next_head_point)
            self.tail_points.append(next_tail_point)
    
    @property
    def w(self):
        return max([point.x for point in self.head_points + self.tail_points]) + 1

    @property
    def h(self):
        return max([point.y for point in self.head_points + self.tail_points]) + 1
    

    def print_points_at(self, i):
        head_point = self.head_points[i]
        tail_point = self.tail_points[i]

        line = ''
        for j in range(self.h):
            for i in range(self.w):
                pos = (i, j)

                point_at_pos = None
                if pos == self.start_point.pos:
                    point_at_pos = self.start_point
                if pos == tail_point.pos:
                    point_at_pos = tail_point
                if pos == head_point.pos:
                    point_at_pos = head_point

                line += str(point_at_pos.mark) if point_at_pos else '.'

            print(line)
            line = ''

    def print(self):
        for i in range(len(self.head_points)):
            self.print_points_at(i)
            print()


class Y2022D09Solver(BaseSolver):
    def solve_part_a(self):
        grid = Grid()
        for line in self.lines:
            grid.move(line)
        return len(set([point.pos for point in grid.tail_points]))
    

    def solve_part_b(self):
        return None
