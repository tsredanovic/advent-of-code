from basesolver import BaseSolver

class Stack:
    def __init__(self, id) -> None:
        self.id = id
        self.crates = []
    
    def add_crate(self, crate: str) -> None:
        self.crates.append(crate)
    
    def remove_crate(self):
        return self.crates.pop()

    def __str__(self) -> str:
        return str('{}:{}'.format(self.id, self.crates))
    
    def __repr__(self) -> str:
        return str(self)

def create_stacks(stacks_lines):
    stacks = {}
    for stack_line_i, stack_line in enumerate(stacks_lines):
        current_i = 1
        while current_i <= len(stack_line):
            value = stack_line[current_i]
            if value == ' ':
                current_i += 4
                continue

            if stack_line_i == 0:
                value = int(value)
                stacks[value] = Stack(value)
            else:
                stack_id = int(stacks_lines[0][current_i])
                stack = stacks[stack_id]
                stack.add_crate(value)
            current_i += 4
    return stacks

def parse_move_line(move_line):
    ids_str = move_line.split(' from ')[1]
    from_id = int(ids_str.split(' to ')[0])
    to_id = int(ids_str.split(' to ')[1])
    count_str = move_line.split(' from ')[0]
    count = int(count_str.split(' ')[1])
    return from_id, to_id, count


def move_crates(stacks, from_id, to_id, count, multiple=False):
    from_stack = stacks[from_id]
    to_stack = stacks[to_id]
    removed_crates = []
    for _ in range(count):
        removed_crate = from_stack.remove_crate()
        removed_crates.append(removed_crate)
    if multiple:
        removed_crates.reverse()
    for crate in removed_crates:
        to_stack.add_crate(crate)

def get_top_crates(stacks):
    ids = [id for id in stacks.keys()]
    ids.sort()
    top_crates = []
    for id in ids:
        stack = stacks[id]
        top_crate = stack.crates[-1]
        top_crates.append(top_crate)
    return top_crates

class Y2022D05Solver(BaseSolver):
    def solve_part_a(self):
        stacks_lines = self.chunks()[0]
        stacks_lines.reverse()
        stacks = create_stacks(stacks_lines)

        moves_lines = self.chunks()[1]
        for move_line in moves_lines:
            from_id, to_id, count = parse_move_line(move_line)
            move_crates(stacks, from_id, to_id, count)

        top_crates = get_top_crates(stacks)
        return ''.join(top_crates)

    def solve_part_b(self):
        stacks_lines = self.chunks()[0]
        stacks_lines.reverse()
        stacks = create_stacks(stacks_lines)

        moves_lines = self.chunks()[1]
        for move_line in moves_lines:
            from_id, to_id, count = parse_move_line(move_line)
            move_crates(stacks, from_id, to_id, count, multiple=True)

        top_crates = get_top_crates(stacks)
        return ''.join(top_crates)
