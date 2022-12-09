from advent_of_code.basesolver import BaseSolver

from collections import defaultdict


class Computer:
    def __init__(self):
        self.current_position = 0
        self.commands = defaultdict(int)

        self.current_input_position = 0
        self.inputs = []

        self.current_relative_position = 0

        self.outputs = []

    def restart(self):
        self.current_position = 0
        self.commands = defaultdict(int)

        self.current_input_position = 0
        self.inputs = []

        self.current_relative_position = 0

        self.outputs = []

    def load_commands(self, commands):
        for i, command in enumerate(commands):
            self.commands[i] = command

    def load_inputs(self, inputs):
        self.current_input_position = 0
        self.inputs = inputs

    def change_cmd_at_pos_1_and_2(self, param1, param2):
        self.commands[1] = param1
        self.commands[2] = param2

    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_POSITION = 9
    HALT = 99
    DESCRIPTION = {
        ADD: 'ADD',
        MULTIPLY: 'MULTIPLY',
        INPUT: 'INPUT',
        OUTPUT: 'OUTPUT',
        JUMP_IF_TRUE: 'JUMP_IF_TRUE',
        JUMP_IF_FALSE: 'JUMP_IF_FALSE',
        LESS_THAN: 'LESS_THAN',
        EQUALS: 'EQUALS',
        ADJUST_RELATIVE_POSITION: 'ADJUST_RELATIVE_POSITION',
        HALT: 'HALT',
    }

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    def read_params(self, num_of_params):
        params = []
        for i in range(1, num_of_params+1):
            params.append(self.commands[self.current_position + i])
        return params

    def get_value_based_on_mode(self, mode, param):
        if mode == self.POSITION_MODE:
            return self.commands[param]
        elif mode == self.IMMEDIATE_MODE:
            return param
        elif mode == self.RELATIVE_MODE:
            return self.commands[self.current_relative_position + param]

    def get_save_at_based_on_mode(self, mode, param):
        save_at = param
        if mode == self.RELATIVE_MODE:
            save_at += self.current_relative_position
        return save_at

    def execute_opcode_action(self, opcode, modes):
        #print('\tOpcode: {} ({}) | Modes: {}'.format(opcode, self.DESCRIPTION[opcode], modes))
        if opcode == self.HALT:
            self.result = self.commands[0]
            #print('\tHALT')
        elif opcode == self.ADD:
            """
            Opcode 1 adds together numbers read from two positions and stores the result in a third position.
            The three integers immediately after the opcode tell you these three positions
            - the first two indicate the positions from which you should read the input values, 
            and the third indicates the position at which the output should be stored.
            """
            num_of_params = 3
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])
            value1 = self.get_value_based_on_mode(modes[1], params[1])
            save_at = self.get_save_at_based_on_mode(modes[2], params[2])

            self.commands[save_at] = value0 + value1

            self.current_position += num_of_params + 1

        elif opcode == self.MULTIPLY:
            """
            Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
            Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
            """
            num_of_params = 3
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])
            value1 = self.get_value_based_on_mode(modes[1], params[1])
            save_at = self.get_save_at_based_on_mode(modes[2], params[2])

            self.commands[save_at] = value0 * value1

            self.current_position += num_of_params + 1

        elif opcode == self.INPUT:
            """
            Opcode 3 takes a single integer as input and saves it to the address given by its only parameter. 
            For example, the instruction 3,50 would take an input value and store it at address 50.
            """
            num_of_params = 1
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            save_at = self.get_save_at_based_on_mode(modes[0], params[0])

            self.commands[save_at] = self.inputs[self.current_input_position]
            self.current_input_position += 1

            self.current_position += num_of_params + 1

        elif opcode == self.OUTPUT:
            """
            Opcode 4 outputs the value of its only parameter. 
            For example, the instruction 4,50 would output the value at address 50.
            """
            num_of_params = 1
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])

            self.outputs.append(value0)

            self.current_position += num_of_params + 1

        elif opcode == self.JUMP_IF_TRUE:
            """
            Opcode 5 is jump-if-true: 
            if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. 
            Otherwise, it does nothing.
            """
            num_of_params = 2
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])
            value1 = self.get_value_based_on_mode(modes[1], params[1])

            if value0 != 0:
                self.current_position = value1
            else:
                self.current_position += num_of_params + 1

        elif opcode == self.JUMP_IF_FALSE:
            """
            Opcode 6 is jump-if-false: 
            if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. 
            Otherwise, it does nothing.
            """
            num_of_params = 2
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])
            value1 = self.get_value_based_on_mode(modes[1], params[1])

            if value0 == 0:
                self.current_position = value1
            else:
                self.current_position += num_of_params + 1

        elif opcode == self.LESS_THAN:
            """
            Opcode 7 is less than: 
            if the first parameter is less than the second parameter, 
            it stores 1 in the position given by the third parameter. 
            Otherwise, it stores 0.
            """
            num_of_params = 3
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])
            value1 = self.get_value_based_on_mode(modes[1], params[1])
            save_at = self.get_save_at_based_on_mode(modes[2], params[2])

            if value0 < value1:
                self.commands[save_at] = 1
            else:
                self.commands[save_at] = 0

            self.current_position += num_of_params + 1

        elif opcode == self.EQUALS:
            """
            Opcode 8 is equals: 
            if the first parameter is equal to the second parameter, 
            it stores 1 in the position given by the third parameter. 
            Otherwise, it stores 0.
            """
            num_of_params = 3
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])
            value1 = self.get_value_based_on_mode(modes[1], params[1])
            save_at = self.get_save_at_based_on_mode(modes[2], params[2])

            if value0 == value1:
                self.commands[save_at] = 1
            else:
                self.commands[save_at] = 0

            self.current_position += num_of_params + 1

        elif opcode == self.ADJUST_RELATIVE_POSITION:
            """
            Opcode 9 adjusts the relative base by the value of its only parameter. 
            The relative base increases (or decreases, if the value is negative) 
            by the value of the parameter.
            """
            num_of_params = 1
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])

            self.current_relative_position += value0

            self.current_position += num_of_params + 1

        else:
            print('INVALID OPCODE: {}'.format(opcode))
            exit(-1)


    def extract_opcode(self, instruction):
        instruction_str = str(instruction).zfill(5)
        return int(instruction_str[-2:])

    def extract_modes(self, instruction):
        instruction_str = str(instruction).zfill(5)
        modes = [int(x) for x in instruction_str[:3]]
        modes.reverse()
        return modes

    def process_commands(self):
        while True:
            #commands_before = list(enumerate(self.commands))
            #print(commands_before)

            current_instruction = self.commands[self.current_position]
            #print('Position: {} | Instruction: {}'.format(self.current_position, current_instruction))
            current_opcode = self.extract_opcode(current_instruction)
            current_modes = self.extract_modes(current_instruction)
            self.execute_opcode_action(current_opcode, current_modes)
            if current_opcode == self.HALT:
                return True

            #commands_after = list(enumerate(self.commands))
            #print(set(commands_after) - set(commands_before))


def load_input(data):
    return [int(x.strip()) for x in data.split(',')]


class Y2019D09Solver(BaseSolver):
    def solve_part_a(self):
        input_list = load_input(self.data)

        computer = Computer()
        computer.load_commands(input_list)
        computer.load_inputs([1])
        succ = computer.process_commands()
        return computer.outputs[-1]

    

    def solve_part_b(self):
        input_list = load_input(self.data)

        computer = Computer()
        computer.load_commands(input_list)
        computer.load_inputs([2])
        succ = computer.process_commands()
        return computer.outputs[-1]

