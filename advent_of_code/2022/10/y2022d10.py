from advent_of_code.basesolver import BaseSolver


class Cmd:
    def __init__(self, input) -> None:
        self.input = input
        split_input = input.split(" ")
        self.cmd = split_input[0]
        self.arg = split_input[1] if len(split_input) > 1 else None

    def __str__(self) -> str:
        return self.input

    def __repr__(self) -> str:
        return str(self)

    def cmds_from_input(lines):
        cmds = []
        for line in lines:
            cmds.append(Cmd(input=line))
        return cmds


class DeviceState:
    def __init__(self, cycle, X) -> None:
        self.cycle = cycle
        self.X = X

    def __str__(self) -> str:
        return "({}, {})".format(self.cycle, self.X)

    def __repr__(self) -> str:
        return str(self)


class Device:
    def __init__(self) -> None:
        self.cycle = 1
        self.X = 1
        self.states = []
        self.save_state()

    def save_state(self):
        self.states.append(DeviceState(self.cycle, self.X))

    def execute_cmd(self, cmd):
        if cmd.cmd == "noop":
            self.execute_noop_cmd(cmd)
        elif cmd.cmd == "addx":
            self.execute_addx_cmd(cmd)

    def execute_noop_cmd(self, cmd):
        self.cycle += 1
        self.save_state()

    def execute_addx_cmd(self, cmd):
        self.cycle += 1
        self.save_state()

        self.cycle += 1
        self.X += int(cmd.arg)
        self.save_state()


class Screen:
    def __init__(self) -> None:
        self.w = 40
        self.h = 6
        self.values = {}
        for y in range(self.h):
            for x in range(self.w):
                self.values[(x, y)] = "?"

    def set_value(self, x, y, value):
        self.values[(x, y)] = value

    def print(self):
        line = ""
        for y in range(self.h):
            for x in range(self.w):
                value = self.values[(x, y)]
                line += str(value)
            print(line)
            line = ""

    def print_str(self):
        lines = []
        line = ""
        for y in range(self.h):
            for x in range(self.w):
                value = self.values[(x, y)]
                line += str(value)
            lines.append(line)
            line = ""
        return "\n".join(lines)


class Y2022D10Solver(BaseSolver):
    def solve_part_a(self):
        cmds = Cmd.cmds_from_input(self.lines)
        device = Device()

        for cmd in cmds:
            device.execute_cmd(cmd)

        result = 0
        for state in device.states:
            # print(state)
            if state.cycle == 20 or (state.cycle - 20) % 40 == 0:
                to_add = state.cycle * state.X
                # print('-- {}'.format(to_add))
                result += to_add
        return result

    def solve_part_b(self):
        cmds = Cmd.cmds_from_input(self.lines)
        device = Device()
        screen = Screen()
        for cmd in cmds:
            device.execute_cmd(cmd)

        y = 0
        for state in device.states:
            x = (state.cycle-1) % 40
            draw_pixel_at = (x, y)
            #print(state, draw_pixel_at)
            sprite_positions = [(state.X - 1, y), (state.X, y), (state.X + 1, y)]
            value = "#" if draw_pixel_at in sprite_positions else "."
            screen.set_value(draw_pixel_at[0], draw_pixel_at[1], value)

            if state.cycle % 40 == 0 and state.cycle != 0:
                y += 1
        return screen.print_str()
