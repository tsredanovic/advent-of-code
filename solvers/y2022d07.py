from basesolver import BaseSolver


class Cmd:
    def __init__(self, input, output) -> None:
        self.input = input
        self.cmd = input.split(' ')[0]
        self.args = input.split(' ')[1:]
        self.output = output
    
    def __str__(self) -> str:
        return '{} -> {}'.format(self.input, self.output)
    
    def __repr__(self) -> str:
        return str(self)
    
    def cmds_from_input(lines):
        cmds = []
        cmd_lines = []
        for line in lines:
            if line.startswith('$') and cmd_lines:
                cmds.append(Cmd(
                    input=cmd_lines[0].lstrip('$ '),
                    output=cmd_lines[1:]
                ))
                cmd_lines = [line]
            else:
                cmd_lines.append(line)
        if cmd_lines:
            cmds.append(Cmd(
                input=cmd_lines[0].lstrip('$ '),
                output=cmd_lines[1:]
            ))
        return cmds


class File:
    def __init__(self, path, size) -> None:
        self.path = path
        self.size = size

    def get_size(self):
        return self.size

    def __str__(self) -> str:
        return '{} -> {}'.format(self.path, self.size)
    
    def __repr__(self) -> str:
        return str(self)


class Directory:
    def __init__(self, path) -> None:
        self.path = path
        self.children = []
    
    def add_child(self, file):
        self.children.append(file)

    def get_size(self):
        size = 0
        for child in self.children:
            size += child.get_size()
        return size

    def __str__(self) -> str:
        return '{}'.format(self.path)
    
    def __repr__(self) -> str:
        return str(self)
    
    def print_with_children(self):
        print('- {}'.format(self.path))
        for child in self.children:
            print('  - {}'.format(child.path))


class Terminal:
    def __init__(self) -> None:
        self.position = None
        self.directories = {}
    
    def execute_cmd(self, cmd):
        #print('Executing: {}'.format(cmd))
        if cmd.cmd == 'cd':
            self.execute_cd_cmd(cmd)
        elif cmd.cmd == 'ls':
            self.execute_ls_cmd(cmd)
        #print('  Position: {}'.format(self.position))
        #print('  Direcotories: {}'.format(self.directories))

    def execute_cd_cmd(self, cmd):
        arg = cmd.args[0]
        if arg == '..':
            for i, char in enumerate(reversed(self.position[:-1])):
                if char == '/':
                    break
            self.position = self.position[0: len(self.position) - i - 1]
        else:
            self.position = self.position + arg if self.position else arg

        if not self.position.endswith('/'):
            self.position += '/'

        if self.position not in self.directories.keys():
            self.directories[self.position] = Directory(self.position)
    
    def execute_ls_cmd(self, cmd):
        for line in cmd.output:
            if line.split(' ')[0].isdigit(): # File
                file_path = '{}{}'.format(self.position, line.split(' ')[1])
                file_size = int(line.split(' ')[0])
                file = File(file_path, file_size)
                self.directories[self.position].add_child(file)
            elif line.split(' ')[0] == 'dir': # Dir
                dir_path = '{}{}/'.format(self.position, ' '.join(line.split(' ')[1:]))
                if dir_path not in self.directories.keys():
                    dir = Directory(dir_path)
                    self.directories[dir_path] = dir
                    self.directories[self.position].add_child(dir)


class Y2022D07Solver(BaseSolver):
    def solve_part_a(self):
        cmds = Cmd.cmds_from_input(self.lines)
        terminal = Terminal()
        for cmd in cmds:
            terminal.execute_cmd(cmd)
        result = 0
        for dir in terminal.directories.values():
            dir_size = dir.get_size()
            if dir_size <= 100000:
                result += dir_size
        return result

    def solve_part_b(self):
        cmds = Cmd.cmds_from_input(self.lines)
        terminal = Terminal()
        for cmd in cmds:
            terminal.execute_cmd(cmd)

        space_total = 70000000
        space_needed = 30000000
        space_used = terminal.directories['/'].get_size()
        space_unused = space_total - space_used
        space_to_delete = space_needed - space_unused

        dir_sizes = []
        for dir in terminal.directories.values():
            dir_sizes.append(dir.get_size())
        
        for dir_size in sorted(dir_sizes):
            if dir_size >= space_to_delete:
                return dir_size
