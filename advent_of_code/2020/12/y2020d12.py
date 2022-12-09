from advent_of_code.basesolver import BaseSolver
   
def parse_cmd(line):
    action = line[0]
    value = int(line[1:])
    return action, value

class Boat1:
    def __init__(self, cmds):
        self.facing = 0
        self.pos = [0, 0]
        self.cmds = cmds
    
    def run(self):
        #print('Pos: {} | Fac: {}'.format(self.pos, self.facing))
        for cmd in self.cmds:
            #print('Executing: {}'.format(cmd))
            action, value = parse_cmd(cmd)
            self.execute_cmd(action, value)
            #print('Pos: {} | Fac: {}'.format(self.pos, self.facing))
    
    def execute_cmd(self, action, value):
        if action == 'N':
            self.execute_N(value)
        if action == 'S':
            self.execute_S(value)
        if action == 'E':
            self.execute_E(value)
        if action == 'W':
            self.execute_W(value)
        if action == 'L':
            self.execute_L(value)
        if action == 'R':
            self.execute_R(value)
        if action == 'F':
            self.execute_F(value)
    
    def execute_N(self, value):
        self.pos[1] += value
    
    def execute_S(self, value):
        self.pos[1] -= value
    
    def execute_E(self, value):
        self.pos[0] += value
    
    def execute_W(self, value):
        self.pos[0] -= value
    
    def execute_L(self, value):
        self.facing = (self.facing + 360 - value) % 360
    
    def execute_R(self, value):
        self.facing = (self.facing + value) % 360
    
    def execute_F(self, value):
        if self.facing == 0:
            self.execute_E(value)
        elif self.facing == 90:
            self.execute_S(value)
        elif self.facing == 180:
            self.execute_W(value)
        elif self.facing == 270:
            self.execute_N(value)
    
    @property
    def manhattan_distance(self):
        return abs(self.pos[0]) + abs(self.pos[1])

class Boat2(Boat1):
    def __init__(self, cmds):
        self.waypoint = [10, 1]
        self.pos = [0, 0]
        self.cmds = cmds

    def run(self):
        #print('Pos: {} | WP: {}'.format(self.pos, self.waypoint))
        for cmd in self.cmds:
            #print('Executing: {}'.format(cmd))
            action, value = parse_cmd(cmd)
            self.execute_cmd(action, value)
            #print('Pos: {} | WP: {}'.format(self.pos, self.waypoint))
    
    def execute_N(self, value):
        self.waypoint[1] += value
    
    def execute_S(self, value):
        self.waypoint[1] -= value
    
    def execute_E(self, value):
        self.waypoint[0] += value
    
    def execute_W(self, value):
        self.waypoint[0] -= value
    
    cos_dict = {
        0: 1,
        90: 0,
        180: -1,
        270: 0
    }
    sin_dict = {
        0: 0,
        90: 1,
        180: 0,
        270: -1
    }
    def rotate_ccw(point, angle):
        wpx = point[0]
        wpy = point[1]

        next_wpx = Boat2.cos_dict[angle] * wpx - Boat2.sin_dict[angle] * wpy
        next_wpy = Boat2.sin_dict[angle] * wpx + Boat2.cos_dict[angle] * wpy

        return [next_wpx, next_wpy]

    def execute_L(self, value):
        angle = value % 360
        self.waypoint = Boat2.rotate_ccw(self.waypoint, angle)
    
    cw_to_ccw = {
        0: 0,
        90: 270,
        180: 180,
        270: 90
    }
    def execute_R(self, value):
        angle = Boat2.cw_to_ccw[(value % 360)]
        self.waypoint = Boat2.rotate_ccw(self.waypoint, angle)
    
    def execute_F(self, value):
        move_x = self.waypoint[0] * value
        move_y = self.waypoint[1] * value
        self.pos[0] += move_x
        self.pos[1] += move_y
    
    @property
    def manhattan_distance(self):
        return abs(self.pos[0]) + abs(self.pos[1])
    

class Y2020D12Solver(BaseSolver):
    def solve_part_a(self):
        boat = Boat1(self.lines)
        boat.run()
        return str(boat.manhattan_distance)
    

    def solve_part_b(self):
        boat = Boat2(self.lines)
        boat.run()
        return str(boat.manhattan_distance)

