import math
from collections import defaultdict


from basesolver import BaseSolver


class Nanofactory:
    def __init__(self, units):
        self.units = units

    def __str__(self):
        return '{}'.format(self.units)

    def __repr__(self):
        return str(self)

    def unit_by_id(self, id):
        for unit in self.units:
            if unit.id == id:
                return unit
        return None


class Unit:
    def __init__(self, id, q, requires):
        self.id = id
        self.q = q
        self.requires = requires

    def __str__(self):
        return '{} {}: {}'.format(self.q, self.id, self.requires)

    def __repr__(self):
        return str(self)


def create_units(content):
    units = []
    for line in content:
        requires_part = line.split(' => ')[0]
        unit_part = line.split(' => ')[1]

        unit_id = unit_part.split(' ')[1]
        unit_q = int(unit_part.split(' ')[0])

        requires = []
        requirements = requires_part.split(', ')
        for req in requirements:
            req_id = req.split(' ')[1]
            req_q = int(req.split(' ')[0])
            requires.append([req_id, req_q])

        units.append(
            Unit(
                id=unit_id,
                q=unit_q,
                requires=requires
            )
        )

    return units


def load_input(lines):
    return [x.strip() for x in lines]


def to_ore(reqs):
    global nf
    total_ores = 0
    current_reqs = reqs
    extras = defaultdict(int)
    while current_reqs:
        # merge items in current reqs
        current_reqs_dict = {}
        for current_req in current_reqs:
            current_req_id = current_req[0]
            current_req_q = current_req[1]
            if current_req_id not in current_reqs_dict.keys():
                current_reqs_dict[current_req_id] = current_req_q
            else:
                current_reqs_dict[current_req_id] += current_req_q
        current_reqs = []
        for current_req_id, current_req_total_q in current_reqs_dict.items():
            current_reqs.append([current_req_id, current_req_total_q])

        print('\tCurrent reqs: {}'.format(current_reqs))
        # see whats currently required
        c_req = current_reqs.pop(0)
        print('\tTaking: {}'.format(c_req))
        c_req_id = c_req[0]
        c_req_q = c_req[1]

        if c_req_id == 'ORE':
            total_ores += c_req_q
            continue

        # find unit with required id
        unit = nf.unit_by_id(c_req_id)

        # calculate how many units are needed
        imam = extras[c_req_id]
        trebam = c_req_q
        batch = unit.q
        napravim = math.ceil((trebam - imam) / batch)
        ekstra = imam + napravim * batch - trebam
        extras[c_req_id] = ekstra
        current_reqs.extend(unit.requires * napravim)

    return total_ores, extras

nf = None

class Y2019D14Solver(BaseSolver):
    def solve_part_a(self):
        input_lines = load_input(self.lines)

        units = create_units(input_lines)

        nf = Nanofactory(units)
        fuel_unit = nf.unit_by_id('FUEL')

        total_ores = 0
        current_reqs = [['FUEL', 1]]
        extras = defaultdict(int)
        while current_reqs:
            # merge items in current reqs
            current_reqs_dict = {}
            for current_req in current_reqs:
                current_req_id = current_req[0]
                current_req_q = current_req[1]
                if current_req_id not in current_reqs_dict.keys():
                    current_reqs_dict[current_req_id] = current_req_q
                else :
                    current_reqs_dict[current_req_id] += current_req_q
            current_reqs = []
            for current_req_id, current_req_total_q in current_reqs_dict.items():
                current_reqs.append([current_req_id, current_req_total_q])

            print(current_reqs)
            # see whats currently required
            c_req = current_reqs.pop(0)
            print('Taking: {}'.format(c_req))
            c_req_id = c_req[0]
            c_req_q = c_req[1]

            if c_req_id == 'ORE':
                total_ores += c_req_q
                continue

            # find unit with required id
            unit = nf.unit_by_id(c_req_id)

            # calculate how many units are needed
            imam = extras[c_req_id]
            trebam = c_req_q
            batch = unit.q
            napravim = math.ceil((trebam - imam) / batch)
            ekstra = imam + napravim * batch - trebam
            extras[c_req_id] = ekstra
            current_reqs.extend(unit.requires * napravim)


        print('Total ore: {}'.format(total_ores))

        return total_ores
    

    def solve_part_b(self):
        global nf
        input_lines = load_input(self.lines)

        units = create_units(input_lines)

        nf = Nanofactory(units)

        reqs = [['FUEL', 1]]
        total_ores, extras = to_ore(reqs)


        print('Total ore for one fuel: {}'.format(total_ores))
        print('Extras after 1 fuel: {}'.format(extras))

        ores_for_1_fuel = total_ores
        extras_after_one_fuel = []
        for extra_id, extra_q in extras.items():
            if extra_q > 0:
                extras_after_one_fuel.append([extra_q, extra_id])
        print('--------------------------------')
        trillion_ores = 1000000000000
        first_iteration_fuel = int(trillion_ores / ores_for_1_fuel)
        first_iteration_extras = []
        for extra_id, extra_q in extras.items():
            if extra_q > 0:
                first_iteration_extras.append([extra_q * first_iteration_fuel, extra_id])

        print(first_iteration_fuel)
        print(first_iteration_extras)

        print('--------------------------------')
        total_fuel = 0
        current_ores = trillion_ores
        while True:
            if current_ores < ores_for_1_fuel:
                break

            current_fuel = int(current_ores / ores_for_1_fuel)
            total_fuel += current_fuel

            current_total_extras = []
            for extra_id, extra_q in extras.items():
                if extra_q > 0:
                    current_total_extras.append([extra_id, extra_q * current_fuel])

            print('With {} ore I made {} fuel, total fuel is {}.'.format(current_ores, current_fuel, total_fuel))
            print('After making that fuel I have extra: {}'.format(current_total_extras))

            total_ores, extras = to_ore(current_total_extras)
            current_ores -= current_fuel * ores_for_1_fuel

        print('Result: {}'.format(total_fuel))

