from basesolver import BaseSolver


class Computer:
    def __init__(self):
        self.current_position = 0
        self.commands = []
        self.result = None
        self.current_output = None

    def restart(self):
        self.current_position = 0
        self.commands = []
        self.result = None

    def load_commands(self, commands):
        self.commands = commands

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
        HALT: 'HALT',
    }

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    def read_params(self, num_of_params):
        params = []
        for i in range(1, num_of_params+1):
            params.append(self.commands[self.current_position + i])
        return params

    def get_value_based_on_mode(self, mode, param):
        if mode == self.POSITION_MODE:
            return self.commands[param]
        else:
            return param

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

            self.commands[params[2]] = value0 + value1

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

            self.commands[params[2]] = value0 * value1

            self.current_position += num_of_params + 1

        elif opcode == self.INPUT:
            """
            Opcode 3 takes a single integer as input and saves it to the address given by its only parameter. 
            For example, the instruction 3,50 would take an input value and store it at address 50.
            """
            num_of_params = 1
            params = self.read_params(num_of_params)
            #print('\tParams: {}'.format(params))

            self.commands[params[0]] = int(input('Enter input: '))

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

            print('Output: {}'.format(value0))
            self.current_output = value0

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

            if value0 < value1:
                self.commands[params[2]] = 1
            else:
                self.commands[params[2]] = 0

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

            if value0 == value1:
                self.commands[params[2]] = 1
            else:
                self.commands[params[2]] = 0

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
            if self.current_position >= len(self.commands):
                return False

            current_instruction = self.commands[self.current_position]
            #print('Position: {} | Instruction: {}'.format(self.current_position, current_instruction))
            current_opcode = self.extract_opcode(current_instruction)
            current_modes = self.extract_modes(current_instruction)
            self.execute_opcode_action(current_opcode, current_modes)
            if current_opcode == self.HALT:
                return True, self.current_output

            #commands_after = list(enumerate(self.commands))
            #print(set(commands_after) - set(commands_before))


def load_input(data):
    return [int(x.strip()) for x in data.split(',')]



class Y2019D05Solver(BaseSolver):
    def solve_part_a(self):
        input_list = load_input(self.data)

        computer = Computer()
        computer.load_commands(input_list)
        succ, current_output = computer.process_commands()

        return current_output
    

    def solve_part_b(self):
        input_list = load_input(self.data)

        computer = Computer()
        computer.load_commands(input_list)
        succ, current_output = computer.process_commands()

        return current_output


