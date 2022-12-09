from advent_of_code.basesolver import BaseSolver

def fuel_from_mass(mass):
    return int(mass/3)-2

class Y2019D01Solver(BaseSolver):
    def solve_part_a(self):
        total_fuel = 0
        for module_mass in self.numbers:
            total_fuel += fuel_from_mass(module_mass)

        return total_fuel

    

    def solve_part_b(self):
        total_fuel = 0
        for module_mass in self.numbers:
            fuel_mass = fuel_from_mass(module_mass)
            while fuel_mass > 0:
                total_fuel += fuel_mass
                fuel_mass = fuel_from_mass(fuel_mass)

        return total_fuel

