from basesolver import BaseSolver


def get_planet_by_id(planets, id):
    for planet in planets:
        if planet.id == id:
            return planet
    return None


class Planet:
    def __init__(self, id, parent):
        self.id = id
        self.parent = parent

    def depth(self):
        depth = 0
        current_planet = self
        while True:
            if not current_planet.parent:
                break
            depth += 1
            current_planet = current_planet.parent
        return depth

    def get_neighbours(self, planets):
        neighbours = []
        for planet in planets:
            if self == planet.parent or planet == self.parent:
                neighbours.append(planet)
        return neighbours

    def distance_to(self, planets, planet):
        distance = 0
        checked = []
        neighbours = [self]
        while True:
            new_neighbours = []
            neighbours = [neighbour for neighbour in neighbours if neighbour not in checked]
            for neighbour in neighbours:
                if planet.id == neighbour.id:
                    return distance
                checked.append(neighbour)

                new_neighbours.extend(neighbour.get_neighbours(planets))

            distance += 1
            neighbours = new_neighbours

    def __str__(self):
        return '{}->{} ({})'.format(self.id, self.parent.id if self.parent else None, self.depth())

    def __repr__(self):
        return str(self)


def load_input(lines):
    return [x.strip() for x in lines]


def create_planets(content):
    planets = []
    for line in content:
        two_panet_ids = line.split(')')
        parent_id = two_panet_ids[0]
        child_id = two_panet_ids[1]
        parent = get_planet_by_id(planets, parent_id)
        child = get_planet_by_id(planets, child_id)

        if not parent:
            parent = Planet(id=parent_id, parent=None)
            planets.append(parent)

        if not child:
            child = Planet(id=child_id, parent=parent)
            planets.append(child)
        else:
            child.parent = parent

    return planets


class Y2019D06Solver(BaseSolver):
    def solve_part_a(self):
        input_lines = load_input(self.lines)

        planets = create_planets(input_lines)

        total_depth = 0
        for planet in planets:
            total_depth += planet.depth()
        return total_depth


    def solve_part_b(self):
        input_lines = load_input(self.lines)

        planets = create_planets(input_lines)

        planet1 = get_planet_by_id(planets, 'YOU').parent
        planet2 = get_planet_by_id(planets, 'SAN').parent

        return planet1.distance_to(planets, planet2)


