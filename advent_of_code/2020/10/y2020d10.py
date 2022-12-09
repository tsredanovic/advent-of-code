from collections import Counter

from advent_of_code.basesolver import BaseSolver


class AdapterArray:
    OVER = 3
    def __init__(self, joltage_ratings):
        self.joltage_ratings = joltage_ratings
    
    def find_array(self):
        self.joltage_ratings.append(0)
        self.joltage_ratings.append(max(self.joltage_ratings) + 3)
        sorted_joltage_ratings = sorted(self.joltage_ratings)
        adapter_array = [0]
        for i in range(1, len(sorted_joltage_ratings)):
            rating1 = sorted_joltage_ratings[i-1]
            rating2 = sorted_joltage_ratings[i]
            if rating2 - rating1 > AdapterArray.OVER:
                return adapter_array
            adapter_array.append(rating2)
        return adapter_array
    
    def find_differences(self):
        adapter_array = self.find_array()
        diffs = []
        for i in range(1, len(adapter_array)):
            rating1 = adapter_array[i-1]
            rating2 = adapter_array[i]
            diffs.append(rating2 - rating1)
        return diffs
    
    def count_differences(self):
        diffs = self.find_differences()
        return Counter(diffs)
    
    def arrangements_num(self):
        aa = self.find_array()
        max_in_aa = max(aa)
        ways_to = {0: 1}
        for i in range(1, max_in_aa + 1):
            if i not in aa:
                ways_to[i] = 0
            else:
                ways_to[i] = ways_to.get(i-1, 0) + ways_to.get(i-2, 0) + ways_to.get(i-3, 0)
        return ways_to[max_in_aa]


class Y2020D10Solver(BaseSolver):
    def solve_part_a(self):
        joltage_ratings = [int(line) for line in self.lines]
        aa = AdapterArray(joltage_ratings)
        counter = aa.count_differences()
        result = counter[1] * counter[3]
        return str(result)
    

    def solve_part_b(self):
        joltage_ratings = [int(line) for line in self.lines]
        aa = AdapterArray(joltage_ratings)
        return str(aa.arrangements_num())

