from advent_of_code.basesolver import BaseSolver

MAX_INT = 2**10000

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

        for pos in [pos for pos in self.sensors.keys()] + [pos for pos in self.beacons.keys()]:
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
                line += char
            lines.append(line)
            line = ""
        print("\n".join(lines))


class Y2022D15Solver(BaseSolver):
    def solve_part_a(self):
        map = Map.map_from_lines(self.lines)
        map.print()

    def solve_part_b(self):
        return None
