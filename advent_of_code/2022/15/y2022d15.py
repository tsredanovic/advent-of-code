from advent_of_code.basesolver import BaseSolver

MAX_INT = 2**10000


def manhattan_distance_2d(p1, p2):
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)


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


class Sensor(Point):
    def __init__(self, x, y, closest_beacon) -> None:
        self.x = x
        self.y = y
        self.closest_beacon = closest_beacon
        self.closest_beacon_manhattan_distance = manhattan_distance_2d(self, closest_beacon)

        self.no_beacon_points = {}
        for d in range(self.closest_beacon_manhattan_distance + 1):
            inverse_d = self.closest_beacon_manhattan_distance - d
            y_up = self.y - d
            y_down = self.y + d
            x_left = self.x - inverse_d
            x_right = self.x + inverse_d
            for x in range(x_left, x_right + 1):
                point = Point(x, y_up)
                if point.pos not in self.no_beacon_points.keys():
                    self.no_beacon_points[point.pos] = point
                point = Point(x, y_down)
                if point.pos not in self.no_beacon_points.keys():
                    self.no_beacon_points[point.pos] = point

class Beacon(Point):
    pass

class Map:
    def __init__(self, sensors, beacons) -> None:
        self.sensors = sensors
        self.beacons = beacons

        self.min_x = MAX_INT
        self.max_x = -MAX_INT
        self.min_y = MAX_INT
        self.max_y = -MAX_INT

        self.no_beacon_points = {}
        for sensor in self.sensors.values():
            for no_beacon_point in sensor.no_beacon_points.values():
                if no_beacon_point.pos not in self.no_beacon_points.keys():
                    new_no_beacon_point = Point(no_beacon_point.x, no_beacon_point.y)
                    self.no_beacon_points[new_no_beacon_point.pos] = new_no_beacon_point


        for pos in [pos for pos in self.sensors.keys()] + [pos for pos in self.beacons.keys()] + [pos for pos in self.no_beacon_points.keys()]:
            x = pos[0]
            y = pos[1]
            if x < self.min_x:
                self.min_x = x
            if x > self.max_x:
                self.max_x = x
            if y < self.min_y:
                self.min_y = y
            if y > self.max_y:
                self.max_y = y
    
    def no_beacon_points_count_at_y(self, y):
        count = 0
        for pos in self.no_beacon_points.keys():
            if pos[1] == y and not self.beacons.get(pos):
                count += 1
        return count

    def map_from_lines(lines):
        sensors = {}
        beacons = {}
        for line in lines:
            beacon_str = line.split(':')[1]
            beacon_x = int(beacon_str.split(' ')[-2].split('=')[1].strip(','))
            beacon_y = int(beacon_str.split(' ')[-1].split('=')[1])
            beacon_pos = (beacon_x, beacon_y)
            if beacon_pos not in beacons.keys():
                beacon = Beacon(beacon_x, beacon_y)
                beacons[beacon.pos] = beacon
            else:
                beacon = beacons[beacon_pos]

            senson_str = line.split(':')[0]
            sensor_x = int(senson_str.split(' ')[-2].split('=')[1].strip(','))
            sensor_y = int(senson_str.split(' ')[-1].split('=')[1])
            sensor_pos = (sensor_x, sensor_y)
            if sensor_pos not in sensors.keys():
                sensor = Sensor(sensor_x, sensor_y, closest_beacon=beacon)
                sensors[sensor.pos] = sensor
            else:
                sensor = sensors[sensor_pos]
        
        return Map(sensors, beacons)

    def print(self):
        lines = []
        line = ""
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                pos = (x, y)
                char = '.'
                if self.sensors.get(pos):
                    char = 'S'
                elif self.beacons.get(pos):
                    char = 'B'
                elif self.no_beacon_points.get(pos):
                    char = '#'
                line += char
            lines.append(line)
            line = ""
        print("\n".join(lines))


class Y2022D15Solver(BaseSolver):
    def solve_part_a(self):
        y = 2000000
        map = Map.map_from_lines(self.lines)
        return map.no_beacon_points_count_at_y(y)

    def solve_part_b(self):
        return None
