
from basesolver import BaseSolver


class Slope:
    def __init__(self, move_x, move_y):
        self.move_x = move_x
        self.move_y = move_y

    def __str__(self):
        return (self.move_x, self.move_y)

    def __repr__(self):
        return self.__str__()


class TreeMap:
    TREE_CHAR = '#'
    BLANK_CHAR = '.'

    def __init__(self, lines):
        self.w = len(lines[0])
        self.h = len(lines)
        self.trees_dict = self.read_where_trees_are(lines, self.w, self.h)
    
    def read_where_trees_are(self, lines, w, h):
        trees_dict = {}
        for i in range(w):
            for j in range(h):
                pos = (i, j)
                char_at_pos = lines[j][i]
                if char_at_pos == self.TREE_CHAR:
                    trees_dict[pos] = 1
                elif char_at_pos == self.BLANK_CHAR:
                    trees_dict[pos] = 0
        return trees_dict
    
    def is_tree_at(self, pos):
        x = pos[0]
        x = x % self.w
        y = pos[1]
        if self.trees_dict[(x, y)]:
            return True
        else:
            return False
    
    def __str__(self):
        tree_map = ''
        for j in range(self.h):
            for i in range(self.w):
                pos = (i, j)
                if self.is_tree_at(pos):
                    tree_map += self.TREE_CHAR
                else:
                    tree_map += self.BLANK_CHAR
            
            tree_map += '\n'
        return tree_map


    
    def __repr__(self):
        return self.__str__()


class Y2020D03Solver(BaseSolver):
    def check_slope(self, tree_map, current_pos, move_x, move_y):
        trees_counter = 0
        while current_pos[1] < tree_map.h:
            x = current_pos[0]
            y = current_pos[1]
            if tree_map.is_tree_at((x, y)):
                trees_counter += 1
            current_pos = (x + move_x, y + move_y)

        return trees_counter


    def solve_part_a(self):
        tree_map = TreeMap(self.lines)
        current_pos = (0, 0)
        slope = Slope(3, 1)
        trees_on_slope = self.check_slope(tree_map, current_pos, slope.move_x, slope.move_y)

        return str(trees_on_slope)
    

    def solve_part_b(self):
        tree_map = TreeMap(self.lines)
        current_pos = (0, 0)
        slopes = [Slope(1, 1), Slope(3, 1), Slope(5, 1), Slope(7, 1), Slope(1, 2)]
        result = 1
        for slope in slopes:
            trees_on_slope = self.check_slope(tree_map, current_pos, slope.move_x, slope.move_y)
            result *= trees_on_slope
        
        return str(result)
