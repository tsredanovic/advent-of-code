import json
from advent_of_code.basesolver import BaseSolver

# 1 - right order
# -1 - wrong order
def compare_lists(l1, l2):
    #print('{} vs {}'.format(l1, l2))

    l1_len = len(l1)
    l2_len = len(l2)

    for i in range(max(l1_len, l2_len)):
        if i == len(l1): # l1 ran out of items
            return 1
        elif i == len(l2): # l2 ran out of items
            return -1
        else:
            v1 = l1[i]
            v2 = l2[i]
            if isinstance(v1, list) or isinstance(v2, list):
                if not isinstance(v1, list):
                    v1 = [v1]
                if not isinstance(v2, list):
                    v2 = [v2]
                result = compare_lists(v1, v2)
                if not result is None:
                    return result
            else:
                if v1 < v2:
                    return 1
                elif v2 < v1:
                    return -1


class Y2022D13Solver(BaseSolver):
    def solve_part_a(self):
        result = 0
        for i, pair in enumerate(self.chunks(), 1):
            pair_result = compare_lists(json.loads(pair[0]), json.loads(pair[1]))
            #print('PAIR {}: {}'.format(i, pair_result))
            if pair_result == 1:
                result += i
        return result

    def solve_part_b(self):
        packets = [json.loads(line) for line in self.lines if line]
        packets.append(json.loads('[[2]]'))
        packets.append(json.loads('[[6]]'))
        iteration = 0
        while iteration == 0 or swap_happened:
            #print('ITERATION {}:'.format(iteration))
            #import pprint
            #pprint.pprint(packets, indent=2)
            swap_happened = False
            for i in range(1, len(packets)):
                left_packet = packets[i-1]
                right_packet = packets[i]
                compare_result = compare_lists(left_packet, right_packet)
                #print('{} vs {} -> {}'.format(left_packet, right_packet, compare_result))
                if  compare_result == -1:
                    packets[i-1] = right_packet
                    packets[i] = left_packet
                    swap_happened = True
                #print(swap_happened)
            iteration += 1

        result = 1
        for i, packet in enumerate(packets, 1):
            if packet == [[2]] or packet == [[6]]:
                result *= i

        return result
