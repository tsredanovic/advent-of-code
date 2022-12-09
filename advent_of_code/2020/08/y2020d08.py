import copy

from advent_of_code.basesolver import BaseSolver


class HGC:

    # states
    STATE_CONT = "cont"
    STATE_INF_LOOP = "inf_loop"
    STATE_TERM = "term"

    # instructions
    INS_ACC = "acc"

    def execute_acc(self, value):
        self.accumulator += value
        self.position += 1

    INS_JMP = "jmp"

    def execute_jmp(self, value):
        self.position += value

    INS_NOP = "nop"

    def execute_nop(self, value):
        self.position += 1

    def parse_instruction(instruction):
        ins_type = instruction.split(" ")[0]
        ins_value = int(instruction.split(" ")[1])
        return ins_type, ins_value

    # works
    def __init__(self, instructions):
        self.instructions = instructions

        self.position = 0
        self.accumulator = 0
        self.executed_instructions_positions = []

    def get_instruction(self):
        return self.instructions[self.position]

    def execute_instruction(self, instruction):
        # Check if instruction was already executed (inf loop)
        if self.position in self.executed_instructions_positions:
            return HGC.STATE_INF_LOOP

        # Add instruction to executed instructions
        self.executed_instructions_positions.append(self.position)

        # Parse instruction
        ins_type, ins_value = HGC.parse_instruction(instruction)

        # Execute instruction
        if ins_type == HGC.INS_ACC:
            self.execute_acc(ins_value)
        elif ins_type == HGC.INS_JMP:
            self.execute_jmp(ins_value)
        elif ins_type == HGC.INS_NOP:
            self.execute_nop(ins_value)

        return HGC.STATE_CONT

    def run(self):
        while True:
            # Check if position is over last instruction by one (terminate)
            if self.position == len(self.instructions):
                return HGC.STATE_TERM, self.accumulator

            # Execute instruction
            instruction = self.get_instruction()
            state = self.execute_instruction(instruction)

            # Check if should continue (cont)
            if state != HGC.STATE_CONT:
                return state, self.accumulator


class Y2020D08Solver(BaseSolver):
    def solve_part_a(self):
        hgc = HGC(self.lines)
        state, accumulator = hgc.run()
        return str(accumulator)

    def solve_part_b(self):
        initial_instructions = self.lines
        tried_change_at_indexes = []
        for index, instruction in enumerate(initial_instructions):
            ins_type, ins_value = HGC.parse_instruction(instruction)
            if (
                ins_type in [HGC.INS_JMP, HGC.INS_NOP]
                and index not in tried_change_at_indexes
            ):
                new_instructions = copy.deepcopy(initial_instructions)
                if ins_type == HGC.INS_JMP:
                    new_ins_type = HGC.INS_NOP
                elif ins_type == HGC.INS_NOP:
                    new_ins_type = HGC.INS_JMP
                new_instruction = " ".join([new_ins_type, str(ins_value)])
                new_instructions[index] = new_instruction

                hgc = HGC(new_instructions)
                state, accumulator = hgc.run()
                if state == HGC.STATE_TERM:
                    return str(accumulator)

                tried_change_at_indexes.append(index)
