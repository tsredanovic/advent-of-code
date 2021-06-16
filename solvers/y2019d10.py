import math
import sys

from basesolver import BaseSolver


class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.asteroids = []

    def is_between(self, asteroid1, asteroid2, asteroid):
        # is asteroid between asteroid1 and asteroid2
        crossproduct = (asteroid.y - asteroid1.y) * (asteroid2.x - asteroid1.x) - (asteroid.x - asteroid1.x) * (asteroid2.y - asteroid1.y)

        # compare versus epsilon for floating point values, or != 0 if using integers
        if abs(crossproduct) > sys.float_info.epsilon:
            return False

        dotproduct = (asteroid.x - asteroid1.x) * (asteroid2.x - asteroid1.x) + (asteroid.y - asteroid1.y) * (asteroid2.y - asteroid1.y)
        if dotproduct < 0:
            return False

        squaredlengthba = (asteroid2.x - asteroid1.x) * (asteroid2.x - asteroid1.x) + (asteroid2.y - asteroid1.y) * (asteroid2.y - asteroid1.y)
        if dotproduct > squaredlengthba:
            return False

        return True

    def does_see(self, asteroid1, asteroid2):
        for asteroid in self.asteroids:
            if asteroid != asteroid1 and asteroid != asteroid2:
                is_between = self.is_between(asteroid1, asteroid2, asteroid)
                if is_between:
                    return False
        return True

    def sees(self, asteroid):
        seen_asteroids = []
        for other_asteroid in self.asteroids:
            if other_asteroid != asteroid:
                if self.does_see(asteroid, other_asteroid):
                    seen_asteroids.append(other_asteroid)
        return seen_asteroids

    def calculate_asteroids_sees(self):
        for i, asteroid in enumerate(self.asteroids, 1):
            asteroid_sees = self.sees(asteroid)
            asteroid.sees = asteroid_sees
            #print('Calculated sees: {}/{}'.format(i, len(self.asteroids)))

    def get_asteroid_by_coords(self, x, y):
        for asteroid in self.asteroids:
            if asteroid.x == x and asteroid.y == y:
                return asteroid
        return None

    def get_all_asteroids_between(self, asteroid1, asteroid2):
        all_asteroids_between = []
        for asteroid in self.asteroids:
            if asteroid != asteroid1 and asteroid != asteroid2:
                if self.is_between(asteroid1, asteroid2, asteroid):
                    all_asteroids_between.append(asteroid)
        return all_asteroids_between

    def distance(self, asteroid1, asteroid2):
        return math.sqrt(((asteroid1.x - asteroid2.x) ** 2) + ((asteroid1.y - asteroid2.y) ** 2))

    def destroy_asteroid(self, asteroid):
        self.asteroids.remove(asteroid)

    def draw(self):
        result = ''
        for y in range(self.h):
            for x in range(self.w):
                map_asteroid = self.get_asteroid_by_coords(x, y)
                if map_asteroid:
                    result += '#'
                else:
                    result += '.'
            result += '\n'
        print(result.strip())

    def draw_asteroid(self, asteroid):
        result = ''
        for y in range(self.h):
            for x in range(self.w):
                map_asteroid = self.get_asteroid_by_coords(x, y)
                if map_asteroid == asteroid:
                    result += 'X'
                elif map_asteroid in asteroid.sees:
                    result += 'O'
                elif map_asteroid:
                    result += '#'
                else:
                    result += '.'
            result += '\n'
        print(result.strip())

    def __str__(self):
        return str(self.asteroids)

    def __repr__(self):
        return str(self)


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sees = None

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return str(self)


def load_input(lines):
    return [x.strip() for x in lines]


def create_map(content):
    map = Map(w=len(content[0]), h=len(content))

    for y, line in enumerate(content):
        for x, char in enumerate(line):
            if char == '#':
                map.asteroids.append(
                    Asteroid(x, y)
                )
    return map


def clockwiseangle_and_distance(point):
    global origin
    global refvec
    # Vector between point and the origin: v = p - o
    vector = [point.x-origin.x, point.y-origin.y]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector


def order_asteroids_clockwise(asteroids):
    global max_sees_asteroid
    sorted_asteroids = sorted(asteroids, key=clockwiseangle_and_distance)
    if sorted_asteroids[0].x == max_sees_asteroid.x:
        return [sorted_asteroids[0]] + list(reversed(sorted_asteroids[1:]))
    else:
        return list(reversed(sorted_asteroids))

max_sees_asteroid = None
origin = None
refvec = None

class Y2019D10Solver(BaseSolver):
    def solve_part_a(self):
        input_content = load_input(self.lines)

        map = create_map(input_content)

        map.calculate_asteroids_sees()

        max_sees_asteroid = map.asteroids[0]
        for asteroid in map.asteroids:
            if len(asteroid.sees) > len(max_sees_asteroid.sees):
                max_sees_asteroid = asteroid

        print('{}: sees {}'.format(max_sees_asteroid, len(max_sees_asteroid.sees)))

        return len(max_sees_asteroid.sees)
    

    def solve_part_b(self):
        global max_sees_asteroid
        global origin
        global refvec
        input_content = load_input(self.lines)

        map = create_map(input_content)

        map.calculate_asteroids_sees()

        max_sees_asteroid = map.asteroids[0]
        for asteroid in map.asteroids:
            if len(asteroid.sees) > len(max_sees_asteroid.sees):
                max_sees_asteroid = asteroid

        print('Station at: {}'.format(max_sees_asteroid))

        origin = max_sees_asteroid
        refvec = [0, -1]

        rotation = 0
        destroyed_asteroids = []
        while True:
            #print('Rotation: {}'.format(rotation))
            #map.draw_asteroid(max_sees_asteroid)
            if len(map.asteroids) == 1:
                break
            clockwise_asteroids = order_asteroids_clockwise(max_sees_asteroid.sees)
            #print('Destroying:', clockwise_asteroids)
            for asteroid in clockwise_asteroids:
                map.destroy_asteroid(asteroid)
                destroyed_asteroids.append(asteroid)

                if len(destroyed_asteroids) == 200:
                    return destroyed_asteroids[-1].x*100 + destroyed_asteroids[-1].y

            map.calculate_asteroids_sees()
            rotation += 1
