import itertools
import math

from advent_of_code.basesolver import BaseSolver


def load_input(lines):
    return [x.strip() for x in lines]


def create_moons(content):
    moons = []
    for line in content:
        xyz = [int(coord.split("=")[1]) for coord in line.strip("<>").split(", ")]
        moons.append(Moon(Position(xyz[0], xyz[1], xyz[2]), Velocity(0, 0, 0)))
    return moons


class Jupiter:
    def __init__(self, moons):
        self.moons = moons

    def __str__(self):
        return "{}".format(self.moons)

    def __repr__(self):
        return str(self)

    def moon_pairs(self):
        return list(itertools.combinations(self.moons, 2))

    def apply_gravities(self):
        """
        To apply gravity, consider every pair of moons.
        On each axis (x, y, and z), the velocity of each moon changes by exactly +1 or -1 to pull the moons together.
        For example, if Ganymede has an x position of 3, and Callisto has a x position of 5,
        then Ganymede's x velocity changes by +1 (because 5 > 3) and Callisto's x velocity changes by -1 (because 3 < 5).
        However, if the positions on a given axis are the same, the velocity on that axis does not change for that pair of moons.
        """
        for moon_pair in self.moon_pairs():
            moon1 = moon_pair[0]
            moon2 = moon_pair[1]

            if moon1.position.x < moon2.position.x:
                moon1.velocity.x += 1
                moon2.velocity.x -= 1
            elif moon1.position.x > moon2.position.x:
                moon1.velocity.x -= 1
                moon2.velocity.x += 1

            if moon1.position.y < moon2.position.y:
                moon1.velocity.y += 1
                moon2.velocity.y -= 1
            elif moon1.position.y > moon2.position.y:
                moon1.velocity.y -= 1
                moon2.velocity.y += 1

            if moon1.position.z < moon2.position.z:
                moon1.velocity.z += 1
                moon2.velocity.z -= 1
            elif moon1.position.z > moon2.position.z:
                moon1.velocity.z -= 1
                moon2.velocity.z += 1

    def apply_velocities(self):
        """
        Simply add the velocity of each moon to its own position.
        For example, if Europa has a position of x=1, y=2, z=3 and a velocity of x=-2, y=0,z=3,
        then its new position would be x=-1, y=2, z=6. This process does not modify the velocity of any moon.
        """
        for moon in self.moons:
            moon.apply_velocity()

    def total_energy(self):
        total_energy = 0
        for moon in self.moons:
            total_energy += moon.total_energy()
        return total_energy

    def hashes_by_plane(self, plane):
        hash = ""
        for moon in self.moons:
            hash += moon.hash_by_plane(plane)
        return hash

    def nice_print(self):
        result = ""
        for moon in self.moons:
            result += str(moon) + "\n"
        result += "Total energy: {}".format(self.total_energy())
        print(result.strip())


class Moon:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __str__(self):
        return "pos={} vel={} pot={} kin={}".format(
            self.position, self.velocity, self.potential_energy(), self.kinetic_energy()
        )

    def __repr__(self):
        return str(self)

    def apply_velocity(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

    def potential_energy(self):
        """
        A moon's potential energy is the sum of the absolute values of its x, y, and z position coordinates.
        """
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    def kinetic_energy(self):
        """
        A moon's kinetic energy is the sum of the absolute values of its velocity coordinates.
        """
        return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

    def total_energy(self):
        """
        The total energy for a single moon is its potential energy multiplied by its kinetic energy.
        """
        return self.potential_energy() * self.kinetic_energy()

    def hash_by_plane(self, plane):
        if plane == "x":
            return "pos={} vel={}".format(self.position.x, self.velocity.x)
        elif plane == "y":
            return "pos={} vel={}".format(self.position.y, self.velocity.y)
        elif plane == "z":
            return "pos={} vel={}".format(self.position.z, self.velocity.z)


class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {} ,{})".format(self.x, self.y, self.z)

    def __repr__(self):
        return str(self)


class Velocity:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {} ,{})".format(self.x, self.y, self.z)

    def __repr__(self):
        return str(self)


def compute_lcm(x, y):
    return abs(x * y) // math.gcd(x, y)


class Y2019D12Solver(BaseSolver):
    def solve_part_a(self):
        input_content = load_input(self.lines)

        moons = create_moons(input_content)

        jupiter = Jupiter(moons)

        step = 0
        while True:
            jupiter.apply_gravities()
            jupiter.apply_velocities()
            step += 1

            if step == 1000:
                print("Step: {}".format(step))
                return jupiter.total_energy()

    def solve_part_b(self):
        input_content = load_input(self.lines)

        steps_for_plane = {}
        for plane in ["x", "y", "z"]:
            moons = create_moons(input_content)

            jupiter = Jupiter(moons)

            previous_jupiters = []

            step = 0
            while True:
                if step % 1000 == 0:
                    print("Step: {}".format(step))
                previous_jupiters.append(jupiter.hashes_by_plane(plane))
                jupiter.apply_gravities()
                jupiter.apply_velocities()
                step += 1

                if jupiter.hashes_by_plane(plane) in previous_jupiters:
                    steps_for_plane[plane] = step
                    print("Step: {} <- {}".format(step, plane))
                    break

        print(steps_for_plane)
        lcm1 = compute_lcm(steps_for_plane["x"], steps_for_plane["y"])
        lcm2 = compute_lcm(lcm1, steps_for_plane["z"])
        return lcm2
