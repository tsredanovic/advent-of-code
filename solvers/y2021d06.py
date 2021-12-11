from basesolver import BaseSolver

def get_next_value(value):
    if value == 0:
        return 6
    else:
        return value - 1

class Y2021D06Solver(BaseSolver):
    def solve_part_a(self):
        fishes = [int(i) for i in self.lines[0].split(',')]

        print('Day 0: {}'.format(fishes))
        for day in range(1, 80 + 1):
            new_fishes = []
            fishes_to_add = 0
            for fish in fishes:
                if fish == 0:
                    fishes_to_add += 1
                new_fish = get_next_value(fish)
                new_fishes.append(new_fish)
            for i in range(fishes_to_add):
                new_fishes.append(8)
            fishes = new_fishes
            print('Day {}'.format(day))

        return len(fishes)

    

    def solve_part_b(self):
        days = 256

        fishes_dict = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0
        }

        fishes = [int(i) for i in self.lines[0].split(',')]
        for fish in fishes:
            fishes_dict[fish] += 1

        for day in range(1, days + 1):
            fishes_to_add_dict = {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 0
            }

            for fish, fish_count in fishes_dict.items():
                if fish == 0:
                    fishes_to_add_dict[8] += fish_count

                new_fish = get_next_value(fish)
                fishes_to_add_dict[new_fish] += fish_count
            
            fishes_dict = fishes_to_add_dict
        
        total = 0
        for fish_count in fishes_dict.values():
            total += fish_count

        return total
