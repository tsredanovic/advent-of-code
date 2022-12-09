from typing import List

from numpy import *

from advent_of_code.basesolver import BaseSolver


class Wire:
    to_add_map = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }

    def __init__(self, input_line) -> None:
        self.points = [(0, 0)]
        inputs = input_line.split(',')
        for input in inputs:
            direction = input[0]
            steps = int(input[1:])
            to_add = self.to_add_map[direction]
            for _ in range(steps):
                self.points.append(
                    (self.points[-1][0] + to_add[0], self.points[-1][1] + to_add[1])
                )
    
    def intersects(self, wire) -> List:
        intersections = []
        for w1_point in self.points:
            if w1_point in wire.points:
                intersections.append(w1_point)
        return intersections


def manhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

    def __repr__(self):
        return str(self)


class Line:
    def __init__(self, point1, point2, orientation):
        self.point1 = point1
        self.point2 = point2
        self.orientation = orientation

        min_x = min(abs(point1.x), abs(point2.x))
        max_x = max(abs(point1.x), abs(point2.x))
        min_y = min(abs(point1.y), abs(point2.y))
        max_y = max(abs(point1.y), abs(point2.y))
        self.length = (max_x - min_x) + (max_y - min_y)

    def __str__(self):
        return '({},{} - {} - {})'.format(self.point1, self.point2, self.orientation, self.length)

    def __repr__(self):
        return str(self)

    def steps(self):
        if self.orientation == 'horizontal':
            min_x = min(self.point1.x, self.point2.x)
            max_x = max(self.point1.x, self.point2.x)
            steps = [(x, self.point1.y) for x in range(min_x, max_x+1)]
            if self.point2.x < self.point1.x:
                steps.reverse()
            return steps
        elif self.orientation == 'vertical':
            min_y = min(self.point1.y, self.point2.y)
            max_y = max(self.point1.y, self.point2.y)
            steps = [(self.point1.x, y) for y in range(min_y, max_y+1)]
            if self.point2.y < self.point1.y:
                steps.reverse()
            return steps


class Intersection:
    def __init__(self, point, line1, line2):
        self.point = point
        self.line1 = line1
        self.line2 = line2
        self.distance_from_0_0 = abs(point.x) + abs(point.y)

    def __str__(self):
        return '{}'.format(self.point)

    def __repr__(self):
        return str(self)


def load_input(lines):
    wire1 = lines[0].strip().split(',')
    wire2 = lines[1].strip().split(',')
    return wire1, wire2


def get_lines(wire):
    lines = []

    c_x, c_y = 0, 0
    for move in wire:
        direction = move[0]
        distance = int(move[1:])

        if direction == 'R':
            n_x = c_x + distance
            n_y = c_y
            orientation = 'horizontal'
        elif direction == 'U':
            n_x = c_x
            n_y = c_y + distance
            orientation = 'vertical'
        elif direction == 'L':
            n_x = c_x - distance
            n_y = c_y
            orientation = 'horizontal'
        elif direction == 'D':
            n_x = c_x
            n_y = c_y - distance
            orientation = 'vertical'

        lines.append(Line(
            Point(c_x, c_y),
            Point(n_x, n_y),
            orientation
        ))

        c_x = n_x
        c_y = n_y

    return lines


def perp(a):
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def seg_intersect(a1, a2, b1, b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    return (num / denom.astype(float))*db + b1


def find_intersections(lines1, lines2):
    intersections = []
    for line1 in lines1:
        for line2 in lines2:
            if line1.orientation != line2.orientation:
                p1 = array([line1.point1.x, line1.point1.y])
                p2 = array([line1.point2.x, line1.point2.y])

                p3 = array([line2.point1.x, line2.point1.y])
                p4 = array([line2.point2.x, line2.point2.y])

                intersection = seg_intersect(p1, p2, p3, p4)

                if intersection[0] == 0 and intersection[1] == 0:
                    continue

                # Check if intersection is on both lines
                intersection_x = int(intersection[0])
                intersection_y = int(intersection[1])

                line1_min_x = min(line1.point1.x, line1.point2.x)
                line1_max_x = max(line1.point1.x, line1.point2.x)
                line1_min_y = min(line1.point1.y, line1.point2.y)
                line1_max_y = max(line1.point1.y, line1.point2.y)

                line2_min_x = min(line2.point1.x, line2.point2.x)
                line2_max_x = max(line2.point1.x, line2.point2.x)
                line2_min_y = min(line2.point1.y, line2.point2.y)
                line2_max_y = max(line2.point1.y, line2.point2.y)

                if line1_min_x <= intersection_x <= line1_max_x and line1_min_y <= intersection_y <= line1_max_y\
                        and line2_min_x <= intersection_x <= line2_max_x and line2_min_y <= intersection_y <= line2_max_y:
                    intersections.append(
                        Intersection(
                            Point(intersection_x, intersection_y),
                            line1,
                            line2
                        )
                    )

    return intersections


def steps_to_intersection(wire1_points, wire2_points, intersection):
    wire1_steps = 0
    for point in wire1_points:
        if point == (intersection.point.x, intersection.point.y):
            break
        wire1_steps += 1
    
    wire2_steps = 0
    for point in wire2_points:
        if point == (intersection.point.x, intersection.point.y):
            break
        wire2_steps += 1
    
    return wire1_steps + wire2_steps


class Y2019D03Solver(BaseSolver):
    def solve_part_a(self):
        wire1, wire2 = load_input(self.lines)
        wire_1_lines = get_lines(wire1)
        wire_2_lines = get_lines(wire2)

        intersections = find_intersections(wire_1_lines, wire_2_lines)

        min_distance = min([intersection.distance_from_0_0 for intersection in intersections])

        return min_distance



        wire1 = Wire(self.lines[0])
        wire2 = Wire(self.lines[1])

        intersections = wire1.intersects(wire2)
        intersections.remove((0,0))
        min_man_intersection = intersections[0]
        min_man_value = manhattan((0, 0), intersections[0])

        for intersection in intersections:
            man_value = manhattan((0, 0), intersection)
            if man_value < min_man_value:
                min_man_intersection = intersection
                min_man_value = man_value
        
        return min_man_intersection[0] + min_man_intersection[1]

    

    def solve_part_b(self):
        wire1, wire2 = load_input(self.lines)
        wire_1_lines = get_lines(wire1)
        wire_2_lines = get_lines(wire2)

        intersections = find_intersections(wire_1_lines, wire_2_lines)

        min_intersection = intersections[0]
        for intersection in intersections:
            if intersection.distance_from_0_0 < min_intersection.distance_from_0_0:
                min_intersection = intersection
        
        wire1_points = Wire(self.lines[0]).points
        wire2_points = Wire(self.lines[1]).points

        min_sti = steps_to_intersection(wire1_points, wire2_points, intersections[0])
        for intersection in intersections:
            sti = steps_to_intersection(wire1_points, wire2_points, intersection)
            if sti < min_sti:
                min_sti = sti

        return min_sti
