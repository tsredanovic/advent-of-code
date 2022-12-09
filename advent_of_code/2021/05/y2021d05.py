from advent_of_code.basesolver import BaseSolver


class Y2021D05Solver(BaseSolver):
    def solve_part_a(self):
        positions_dict = {}
        for line in self.lines:
            p1_str, p2_str = line.split(" -> ")
            x1, y1 = [int(i) for i in p1_str.split(",")]
            x2, y2 = [int(i) for i in p2_str.split(",")]
            positions = []
            if x1 == x2:
                if y1 <= y2:
                    positions = [(x1, i) for i in range(y1, y2 + 1)]
                else:
                    positions = [(x1, i) for i in range(y2, y1 + 1)]
            elif y1 == y2:
                if x1 <= x2:
                    positions = [(i, y1) for i in range(x1, x2 + 1)]
                else:
                    positions = [(i, y1) for i in range(x2, x1 + 1)]
            else:
                continue
            if not positions:
                print("ERROR")
                exit()
            for position in positions:
                if position not in positions_dict.keys():
                    positions_dict[position] = 1
                else:
                    positions_dict[position] += 1
        danger_pos_count = 0
        for value in positions_dict.values():
            if value >= 2:
                danger_pos_count += 1
        return danger_pos_count

    def solve_part_b(self):
        positions_dict = {}
        for line in self.lines:
            p1_str, p2_str = line.split(" -> ")
            x1, y1 = [int(i) for i in p1_str.split(",")]
            x2, y2 = [int(i) for i in p2_str.split(",")]
            positions = []
            if x1 == x2:
                if y1 <= y2:
                    positions = [(x1, i) for i in range(y1, y2 + 1)]
                else:
                    positions = [(x1, i) for i in range(y2, y1 + 1)]
            elif y1 == y2:
                if x1 <= x2:
                    positions = [(i, y1) for i in range(x1, x2 + 1)]
                else:
                    positions = [(i, y1) for i in range(x2, x1 + 1)]
            else:
                bigger_x = x1 if x1 >= x2 else x2
                smaller_x = x2 if x1 >= x2 else x1
                bigger_y = y1 if y1 >= y2 else y2
                smaller_y = y2 if y1 >= y2 else y1
                if smaller_x == x1:
                    add_to_x = 1
                else:
                    add_to_x = -1
                if smaller_y == y1:
                    add_to_y = 1
                else:
                    add_to_y = -1
                for i in range(bigger_x - smaller_x + 1):
                    positions.append((x1 + i * add_to_x, y1 + i * add_to_y))
            if not positions:
                import pdb

                pdb.set_trace()
                print("ERROR")
                exit()
            for position in positions:
                if position not in positions_dict.keys():
                    positions_dict[position] = 1
                else:
                    positions_dict[position] += 1
        danger_pos_count = 0
        for value in positions_dict.values():
            if value >= 2:
                danger_pos_count += 1
        return danger_pos_count
