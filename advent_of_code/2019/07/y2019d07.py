import itertools

from advent_of_code.basesolver import BaseSolver


class Computer:
    def __init__(self):
        self.current_position = 0
        self.commands = []

        self.current_input_position = 0
        self.inputs = []

        self.outputs = []

    def restart(self):
        self.current_position = 0
        self.commands = []

        self.current_input_position = 0
        self.inputs = []

        self.outputs = []

    def load_commands(self, commands):
        self.commands = commands.copy()

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
    HALT = 99
    DESCRIPTION = {
        ADD: "ADD",
        MULTIPLY: "MULTIPLY",
        INPUT: "INPUT",
        OUTPUT: "OUTPUT",
        JUMP_IF_TRUE: "JUMP_IF_TRUE",
        JUMP_IF_FALSE: "JUMP_IF_FALSE",
        LESS_THAN: "LESS_THAN",
        EQUALS: "EQUALS",
        HALT: "HALT",
    }

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    def read_params(self, num_of_params):
        params = []
        for i in range(1, num_of_params + 1):
            params.append(self.commands[self.current_position + i])
        return params

    def get_value_based_on_mode(self, mode, param):
        if mode == self.POSITION_MODE:
            return self.commands[param]
        else:
            return param

    def execute_opcode_action(self, opcode, modes):
        # print('\tOpcode: {} ({}) | Modes: {}'.format(opcode, self.DESCRIPTION[opcode], modes))
        if opcode == self.HALT:
            self.result = self.commands[0]
            # print('\tHALT')
        elif opcode == self.ADD:
            """
            Opcode 1 adds together numbers read from two positions and stores the result in a third position.
            The three integers immediately after the opcode tell you these three positions
            - the first two indicate the positions from which you should read the input values,
            and the third indicates the position at which the output should be stored.
            """
            num_of_params = 3
            params = self.read_params(num_of_params)
            # print('\tParams: {}'.format(params))

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
            # print('\tParams: {}'.format(params))

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
            # print('\tParams: {}'.format(params))

            self.commands[params[0]] = self.inputs[self.current_input_position]
            self.current_input_position += 1

            self.current_position += num_of_params + 1

        elif opcode == self.OUTPUT:
            """
            Opcode 4 outputs the value of its only parameter.
            For example, the instruction 4,50 would output the value at address 50.
            """
            num_of_params = 1
            params = self.read_params(num_of_params)
            # print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])

            self.outputs.append(value0)

            self.current_position += num_of_params + 1

            return value0

        elif opcode == self.JUMP_IF_TRUE:
            """
            Opcode 5 is jump-if-true:
            if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter.
            Otherwise, it does nothing.
            """
            num_of_params = 2
            params = self.read_params(num_of_params)
            # print('\tParams: {}'.format(params))

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
            # print('\tParams: {}'.format(params))

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
            # print('\tParams: {}'.format(params))

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
            # print('\tParams: {}'.format(params))

            value0 = self.get_value_based_on_mode(modes[0], params[0])
            value1 = self.get_value_based_on_mode(modes[1], params[1])

            if value0 == value1:
                self.commands[params[2]] = 1
            else:
                self.commands[params[2]] = 0

            self.current_position += num_of_params + 1

        else:
            print("INVALID OPCODE: {}".format(opcode))
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
            # commands_before = list(enumerate(self.commands))
            # print(commands_before)
            if self.current_position >= len(self.commands):
                return False

            current_instruction = self.commands[self.current_position]
            # print('Position: {} | Instruction: {}'.format(self.current_position, current_instruction))
            current_opcode = self.extract_opcode(current_instruction)
            current_modes = self.extract_modes(current_instruction)
            possible_output = self.execute_opcode_action(current_opcode, current_modes)
            if possible_output:
                return possible_output
            if current_opcode == self.HALT:
                return True

            # commands_after = list(enumerate(self.commands))
            # print(set(commands_after) - set(commands_before))


def load_input(data):
    return [int(x.strip()) for x in data.split(",")]


def test_phase_settings(one_phase_settings, input_list):
    amplifiers = []
    for i in range(5):
        computer = Computer()
        computer.load_commands(input_list)

        amplifiers.append(computer)

    counter = 0
    first_iteration = True
    while True:
        if counter == 5:
            first_iteration = False
        current_index = counter % 5
        # print('Amplifier: {}'.format(current_index))
        previous_index = counter % 5 - 1 if current_index != 0 else 4

        amplifier = amplifiers[current_index]

        first_input = one_phase_settings[current_index]
        second_input = (
            amplifiers[previous_index].outputs[-1]
            if amplifiers[previous_index].outputs
            else 0
        )

        if first_iteration:
            current_inputs = [first_input, second_input]
        else:
            current_inputs = [second_input]

        # print('\tCurrent position: {}'.format(amplifier.current_position))
        # print('\tCommands: {}'.format(amplifier.commands))
        # print('\tInputs: {}'.format(current_inputs))

        amplifier.load_inputs(current_inputs)
        succ = amplifier.process_commands()
        # print('\tProcessing commands...')
        # print('\tCurrent position: {}'.format(amplifier.current_position))
        # print('\tCommands: {}'.format(amplifier.commands))
        # print('\tOutputs: {}'.format(amplifier.outputs))
        if succ == True and amplifier == amplifiers[-1]:
            return amplifiers[-1].outputs[-1]

        counter += 1


class Y2019D07Solver(BaseSolver):
    def solve_part_a(self):
        input_list = load_input(self.data)

        phase_settings_nums = [0, 1, 2, 3, 4]

        all_phase_settings = [
            list(one_phase_settings)
            for one_phase_settings in list(itertools.permutations(phase_settings_nums))
        ]

        final_outputs = {}
        for one_phase_settings in all_phase_settings:

            amplifiers = []
            for i in range(5):
                computer = Computer()
                computer.load_commands(input_list)

                current_output = 0 if i == 0 else amplifiers[i - 1].outputs[0]
                current_inputs = [one_phase_settings[i], current_output]

                computer.load_inputs(current_inputs)
                succ = computer.process_commands()

                amplifiers.append(computer)

            final_outputs[tuple(one_phase_settings)] = amplifiers[-1].outputs[0]

        return max(final_outputs.values())

    def solve_part_b(self):
        input_list = load_input(self.data)

        phase_settings_nums = [5, 6, 7, 8, 9]

        all_phase_settings = [
            list(one_phase_settings)
            for one_phase_settings in list(itertools.permutations(phase_settings_nums))
        ]

        final_outputs = {}
        for one_phase_settings in all_phase_settings:
            try:
                result = test_phase_settings(one_phase_settings, input_list)
            except Exception as e:
                result = 0
            final_outputs[tuple(one_phase_settings)] = result
            print("{} : {}".format(tuple(one_phase_settings), result))

        return max(final_outputs.values())
