from collections import OrderedDict

from advent_of_code.basesolver import BaseSolver

class SeatingSystem:
    SEAT_EMPTY = 'L'
    SEAT_OCC = '#'
    FLOOR = '.'

    def draw_map_dict(map_dict):
        map_w = max(pos[0] for pos in map_dict.keys()) + 1
        map_h = max(pos[1] for pos in map_dict.keys()) + 1

        print_str = ''
        for y in range(map_h):
            for x in range(map_w):
                pos = (x, y)
                value = map_dict[pos]
                print_str += value
            print_str += '\n'
        print_str = print_str.rstrip('\n')
        print(print_str)

    def print_map_dict(map_dict):
        for pos, value in map_dict.items():
            print('{}: {}'.format(pos, value))

    def __init__(self, map_list, part):
        self.map_w = len(map_list[0])
        self.map_h = len(map_list)

        map_dict = OrderedDict()
        for x in range(self.map_w):
            for y in range(self.map_h):
                pos = (x, y)
                value = map_list[y][x]
                map_dict[pos] = value
        
        self.maps = [map_dict]

        self.part = part
    
    def get_adj_positions(pos):
        x = pos[0]
        xs = [x-1, x, x+1]
        y = pos[1]
        ys = [y-1, y, y+1]

        adj_positions = []
        for x in xs:
            for y in ys:
                ajd_pos = (x, y)
                if pos != ajd_pos:
                    adj_positions.append(ajd_pos)
        return adj_positions
    
    def check_if_no_occ(seat_values):
        for seat_value in seat_values:
            if seat_value == SeatingSystem.SEAT_OCC:
                return False
        return True
    
    def check_if_more_than_occ(seat_values, check_count):
        occ_count = 0
        for seat_value in seat_values:
            if seat_value == SeatingSystem.SEAT_OCC:
                occ_count += 1
            if occ_count > check_count:
                return True
        return False
    
    def get_seen_values(self, pos, map_dict):
        pos_x = pos[0]
        pos_y = pos[1]
        min_x = 0
        max_x = self.map_w
        min_y = 0
        max_y = self.map_h

        seen_values = []

        # Go right
        #print('Going right')
        for x in range(pos_x+1, max_x):
            value = map_dict[x, pos_y]
            #print('({}, {}) -> {}'.format(x, pos_y, value))
            seen_values.append(value)
            if value in [SeatingSystem.SEAT_OCC, SeatingSystem.SEAT_EMPTY]:
                break
        
        # Go left
        #print('Going left')
        for x in [_ for _ in range(min_x, pos_x)][::-1]:
            value = map_dict[x, pos_y]
            #print('({}, {}) -> {}'.format(x, pos_y, value))
            seen_values.append(value)
            if value in [SeatingSystem.SEAT_OCC, SeatingSystem.SEAT_EMPTY]:
                break
        
        # Go down
        #print('Going down')
        for y in range(pos_y+1, max_y):
            value = map_dict[pos_x, y]
            #print('({}, {}) -> {}'.format(pos_x, y, value))
            seen_values.append(value)
            if value in [SeatingSystem.SEAT_OCC, SeatingSystem.SEAT_EMPTY]:
                break
        
        # Go up
        #print('Going up')
        for y in [_ for _ in range(min_y, pos_y)][::-1]:
            value = map_dict[pos_x, y]
            #print('({}, {}) -> {}'.format(pos_x, y, value))
            seen_values.append(value)
            if value in [SeatingSystem.SEAT_OCC, SeatingSystem.SEAT_EMPTY]:
                break
        
        # Go right down
        #print('Going right down')
        curr_x = pos_x + 1
        curr_y = pos_y + 1
        while True:
            value = map_dict.get((curr_x, curr_y), None)
            if not value:
                break
            #print('({}, {}) -> {}'.format(x, y, value))
            seen_values.append(value)
            if value in [SeatingSystem.SEAT_OCC, SeatingSystem.SEAT_EMPTY]:
                break
            curr_x += 1
            curr_y += 1
        
        # Go right up
        #print('Going right up')
        curr_x = pos_x + 1
        curr_y = pos_y - 1
        while True:
            value = map_dict.get((curr_x, curr_y), None)
            if not value:
                break
            #print('({}, {}) -> {}'.format(x, y, value))
            seen_values.append(value)
            if value in [SeatingSystem.SEAT_OCC, SeatingSystem.SEAT_EMPTY]:
                break
            curr_x += 1
            curr_y -= 1

        # Go left up
        #print('Going left up')
        curr_x = pos_x - 1
        curr_y = pos_y - 1
        while True:
            value = map_dict.get((curr_x, curr_y), None)
            if not value:
                break
            #print('({}, {}) -> {}'.format(x, y, value))
            seen_values.append(value)
            if value in [SeatingSystem.SEAT_OCC, SeatingSystem.SEAT_EMPTY]:
                break
            curr_x -= 1
            curr_y -= 1
        
        # Go left down
        #print('Going left down')
        curr_x = pos_x - 1
        curr_y = pos_y + 1
        while True:
            value = map_dict.get((curr_x, curr_y), None)
            if not value:
                break
            #print('({}, {}) -> {}'.format(x, y, value))
            seen_values.append(value)
            if value in [SeatingSystem.SEAT_OCC, SeatingSystem.SEAT_EMPTY]:
                break
            curr_x -= 1
            curr_y += 1

        return seen_values

    def get_seat_values(self, pos, map_dict):
        if self.part == 'a':
            adj_positions = SeatingSystem.get_adj_positions(pos)
            return [map_dict.get(adj_pos, '.') for adj_pos in adj_positions]
        else:
            seen_values = self.get_seen_values(pos, map_dict)
            return seen_values
    
    def get_next_value(self, pos, map_dict):
        value = map_dict[pos]
        #print('\tCurrent value: {}'.format(value))

        if value == SeatingSystem.FLOOR:
            return SeatingSystem.FLOOR
    
        interesting_values = self.get_seat_values(pos, map_dict)
        #print('\tInt values: {}'.format(interesting_values))
        
        if value == SeatingSystem.SEAT_EMPTY:
            if SeatingSystem.check_if_no_occ(interesting_values):
                return SeatingSystem.SEAT_OCC
        
        check_count = 3 if self.part == 'a' else 4
        
        if value == SeatingSystem.SEAT_OCC:
            if SeatingSystem.check_if_more_than_occ(interesting_values, check_count):
                return SeatingSystem.SEAT_EMPTY
        
        return value
    
    def calculate_next_map(self, map_dict):
        next_map = OrderedDict()
        for y in range(self.map_h):
            for x in range(self.map_w):
                pos = (x, y)
                #print('Checking {}'.format(pos))
                next_value = self.get_next_value(pos, map_dict)
                #print('\tNext value {}'.format(next_value))
                next_map[(x, y)] = next_value
        
        return next_map
    
    def are_maps_same(self, map_dict_1, map_dict_2):
        for y in range(self.map_h):
            for x in range(self.map_w):
                pos = (x, y)
                if map_dict_1[pos] != map_dict_2[pos]:
                    return False
        return True

    def generate_maps(self):
        self.map_index = 0
        while True:
            current_map_dict = self.maps[self.map_index]
            next_map_dict = self.calculate_next_map(current_map_dict)
            self.maps.append(next_map_dict)

            if self.are_maps_same(current_map_dict, next_map_dict):
                break
            
            self.map_index += 1
    
    def count_value_in_map(map_dict, value):
        map_w = max(pos[0] for pos in map_dict.keys()) + 1
        map_h = max(pos[1] for pos in map_dict.keys()) + 1

        count = 0
        for y in range(map_h):
            for x in range(map_w):
                pos = (x, y)
                if map_dict[pos] == value:
                    count += 1
        return count


class Y2020D11Solver(BaseSolver):
    def solve_part_a(self):
        ss = SeatingSystem(self.lines, self.part)
        ss.generate_maps()
        seat_occ_count = SeatingSystem.count_value_in_map(ss.maps[-1], SeatingSystem.SEAT_OCC)
        return str(seat_occ_count)
    

    def solve_part_b(self):
        ss = SeatingSystem(self.lines, self.part)
        ss.generate_maps()
        seat_occ_count = SeatingSystem.count_value_in_map(ss.maps[-1], SeatingSystem.SEAT_OCC)
        return str(seat_occ_count)

