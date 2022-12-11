from advent_of_code.basesolver import BaseSolver


class Operation:
    OP_MULTIPLY = '*'
    OP_ADD = '+'

    def __init__(self, param1, op, param2) -> None:
        self.param1 = param1
        self.op = op
        self.param2 = param2
    
    def execute(self, old_value):
        param1 = int(self.param1) if self.param1.isdigit() else old_value
        param2 = int(self.param2) if self.param2.isdigit() else old_value
        if self.op == self.OP_MULTIPLY:
            return param1 * param2
        else:
            return param1 + param2

    def __str__(self) -> str:
        return '{} {} {}'.format(self.param1, self.op, self.param2)
    
    def __repr__(self) -> str:
        return str(self)


class Monkey:
    def __init__(self, id, items, operation, test_div_by, test_true_monkey_id, test_false_monkey_id) -> None:
        self.id = id
        self.items = items
        self.operation = operation
        self.test_div_by = test_div_by
        self.test_true_monkey_id = test_true_monkey_id
        self.test_false_monkey_id = test_false_monkey_id
        self.inspection_count = 0

        self.items_factors = []
        for item in self.items:
            item_factors = list(factors(item))
            self.items_factors.append(item_factors)

    def monkey_from_chunk(chunk):
        id = int(chunk[0].split(' ')[1].rstrip(':'))

        starting_items = [int(item_str.strip(',')) for item_str in chunk[1].split(' ')[4:]]

        op_values = chunk[2].split(' ')[5:]
        operation = Operation(op_values[0], op_values[1], op_values[2])

        test_div_by = int(chunk[3].split(' ')[-1])
        test_true_monkey_id = int(chunk[4].split(' ')[-1])
        test_false_monkey_id = int(chunk[5].split(' ')[-1])

        return Monkey(id, starting_items, operation, test_div_by, test_true_monkey_id, test_false_monkey_id)
    
    def __str__(self) -> str:
        return str(self.id)
    
    def __repr__(self) -> str:
        return str(self)
    
    def print(self):
        print('M{} | {} | {} | div by {} ? {} : {}'.format(self.id, self.items, self.operation, self.test_div_by, self.test_true_monkey_id, self.test_false_monkey_id))

    def print_items(self):
        print('M{} | {}'.format(self.id, self.items))

class Y2022D11Solver(BaseSolver):
    def solve_part_a(self):
        ROUND_COUNT = 20

        monkeys = {}
        for chunk in self.chunks():
            monkey = Monkey.monkey_from_chunk(chunk)
            #monkey.print()
            monkeys[monkey.id] = monkey

        monkey_ids_sorted = sorted(monkeys.keys())
        for round in range(ROUND_COUNT):
            #print('ROUND {}'.format(round))
            for monkey_id in monkey_ids_sorted:
                monkey = monkeys[monkey_id]
                monkey_items = monkey.items.copy()
                monkey.items = []
                for item in monkey_items:
                    monkey.inspection_count += 1
                    new_item = int(monkey.operation.execute(item) / 3)
                    if (new_item / monkey.test_div_by).is_integer():
                        throw_to_monkey_id = monkey.test_true_monkey_id
                    else:
                        throw_to_monkey_id = monkey.test_false_monkey_id
                    monkeys[throw_to_monkey_id].items.append(new_item)

            #for monkey_id in monkey_ids_sorted:
            #    monkey = monkeys[monkey_id]
            #    monkey.print_items()
        
        sorted_inspection_counts = sorted(monkey.inspection_count for monkey in monkeys.values())
        return sorted_inspection_counts[-1] * sorted_inspection_counts[-2]

    def solve_part_b(self):
        ROUND_COUNT = 10000

        monkeys = {}
        for chunk in self.chunks():
            monkey = Monkey.monkey_from_chunk(chunk)
            #monkey.print()
            monkeys[monkey.id] = monkey

        monkey_ids_sorted = sorted(monkeys.keys())
        for round in range(ROUND_COUNT):
            #print('ROUND {}'.format(round))
            for monkey_id in monkey_ids_sorted:
                monkey = monkeys[monkey_id]
                monkey_items = monkey.items.copy()
                monkey.items = []
                for item in monkey_items:
                    monkey.inspection_count += 1
                    new_item = monkey.operation.execute(item)
                    if (new_item / monkey.test_div_by).is_integer():
                        throw_to_monkey_id = monkey.test_true_monkey_id
                    else:
                        throw_to_monkey_id = monkey.test_false_monkey_id
                    monkeys[throw_to_monkey_id].items.append(new_item)

            #for monkey_id in monkey_ids_sorted:
            #    monkey = monkeys[monkey_id]
            #    monkey.print_items()
        
        sorted_inspection_counts = sorted(monkey.inspection_count for monkey in monkeys.values())
        return sorted_inspection_counts[-1] * sorted_inspection_counts[-2]
