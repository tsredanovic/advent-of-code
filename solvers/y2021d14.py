from basesolver import BaseSolver

from collections import Counter

def get_char_counts(pairs):
    char_counts = {}
    for pair, pair_count in pairs.items():
        if pair[0] not in char_counts.keys():
            char_counts[pair[0]] = pair_count
        else:
            char_counts[pair[0]] += pair_count
        if pair[1] not in char_counts.keys():
            char_counts[pair[1]] = pair_count
        else:
            char_counts[pair[1]] += pair_count
    return char_counts

class Y2021D14Solver(BaseSolver):
    def solve_part_a(self):
        current_template = self.lines[0]
        rules = {}
        for line in self.lines[2:]:
            rules[line.split(' -> ')[0]] = line.split(' -> ')[1]
        
        steps = 10

        for step in range(1, steps + 1):
            insertions = []
            for i in range(1, len(current_template)):
                pair = current_template[i-1] + current_template[i]
                insertions.append(rules[pair])
            
            insert_at = len(current_template) - 1
            for to_insert in insertions[::-1]:
                current_template = current_template[:insert_at] + to_insert + current_template[insert_at:]
                insert_at -= 1
        
            print('Step {} done.'.format(step))
        counter = Counter(current_template)
        return counter.most_common()[0][1] - counter.most_common()[-1][1]

    def solve_part_b(self):
        steps = 40

        current_template = self.lines[0]
        rules = {}
        for line in self.lines[2:]:
            rules[line.split(' -> ')[0]] = line.split(' -> ')[1]

        current_pairs = {}
        for pair in rules.keys():
            current_pairs[pair] = 0

        for i in range(1, len(current_template)):
            pair = current_template[i-1] + current_template[i]
            current_pairs[pair] += 1

        char_count = {}
        for pair in rules.keys():
            if pair[0] not in char_count.keys():
                char_count[pair[0]] = 0
            if pair[1] not in char_count.keys():
                char_count[pair[1]] = 0
            
        for char in current_template:
            char_count[char] += 1

        #print('Step {} done.'.format(0))
        #print('Char counts: {}'.format(char_count))
        for step in range(1, steps + 1):
            new_pairs = {}
            for pair in rules.keys():
                new_pairs[pair] = 0
            
            for pair, pair_count in current_pairs.items():
                if pair_count == 0:
                    continue
                new_pair_1 = pair[0] + rules[pair]
                new_pair_2 = rules[pair] + pair[1]
                new_pairs[new_pair_1] += pair_count
                new_pairs[new_pair_2] += pair_count
                char_count[rules[pair]] += pair_count
            
            current_pairs = new_pairs
        
            #print('Step {} done.'.format(step))
            #print('Char counts: {}'.format(char_count))
        
        max_char_count = list(char_count.values())[0]
        min_char_count = list(char_count.values())[1]
        for value in char_count.values():
            if value > max_char_count:
                max_char_count = value
            if value < min_char_count:
                min_char_count = value

        return max_char_count - min_char_count
