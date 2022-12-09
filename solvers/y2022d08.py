from advent_of_code.basesolver import BaseSolver


class Grid:
    def __init__(self, w, h) -> None:
        self.w = w
        self.h = h
        self.trees = {}
    
    def add_tree(self, tree):
        if tree.pos in self.trees.keys():
            print('Tree already at position {}!!!'.format(tree.pos))
            exit()
        self.trees[tree.pos] = tree
    
    def get_tree(self, x, y):
        return self.trees[(x, y)]

    def is_tree_left_visible(self, tree):
        if tree.x == 0:
            return True
        
        for x in range(tree.x):
            cmp_tree = self.get_tree(x, tree.y)
            if cmp_tree.h >= tree.h:
                return False

        return True

    def is_tree_right_visible(self, tree):
        if tree.x == self.w - 1:
            return True
        
        for x in range(tree.x+1, self.w):
            cmp_tree = self.get_tree(x, tree.y)
            if cmp_tree.h >= tree.h:
                return False

        return True

    def is_tree_top_visible(self, tree):
        if tree.y == 0:
            return True
        
        for y in range(tree.y):
            cmp_tree = self.get_tree(tree.x, y)
            if cmp_tree.h >= tree.h:
                return False
        
        return True

    def is_tree_bottom_visible(self, tree):
        if tree.y == self.h - 1:
            return True
        
        for y in range(tree.y+1, self.h):
            cmp_tree = self.get_tree(tree.x, y)
            if cmp_tree.h >= tree.h:
                return False

        return True

    def is_tree_visible(self, tree):
        if self.is_tree_left_visible(tree) or self.is_tree_right_visible(tree) or self.is_tree_top_visible(tree) or self.is_tree_bottom_visible(tree):
            return True
        
        return False

    def visible_trees_count(self):
        count = 0
        for j in range(self.h):
            for i in range(self.w):
                tree = self.get_tree(i, j)
                if self.is_tree_visible(tree):
                    count += 1
        return count

    def tree_left_score(self, tree):
        score = 0
        if tree.x == 0:
            return score

        for x in reversed(range(tree.x)):
            score += 1
            cmp_tree = self.get_tree(x, tree.y)
            if cmp_tree.h >= tree.h:
                return score

        return score

    def tree_right_score(self, tree):
        score = 0
        if tree.x == self.w - 1:
            return score
        
        for x in range(tree.x+1, self.w):
            score += 1
            cmp_tree = self.get_tree(x, tree.y)
            if cmp_tree.h >= tree.h:
                return score

        return score

    def tree_top_score(self, tree):
        score = 0
        if tree.y == 0:
            return score
        
        for y in reversed(range(tree.y)):
            score += 1
            cmp_tree = self.get_tree(tree.x, y)
            if cmp_tree.h >= tree.h:
                return score
        
        return score

    def tree_bottom_score(self, tree):
        score = 0
        if tree.y == self.h - 1:
            return score
        
        for y in range(tree.y+1, self.h):
            score += 1
            cmp_tree = self.get_tree(tree.x, y)
            if cmp_tree.h >= tree.h:
                return score

        return score

    def tree_score(self, tree):
        return self.tree_left_score(tree) * self.tree_right_score(tree) * self.tree_top_score(tree) * self.tree_bottom_score(tree)


    def print(self):
        line = ''
        for j in range(self.h):
            for i in range(self.w):
                tree = self.get_tree(i, j)
                line += str(tree.h)
            print(line)
            line = ''
    
    def print_visibility(self):
        line = ''
        for j in range(self.h):
            for i in range(self.w):
                tree = self.get_tree(i, j)
                line += '1' if self.is_tree_visible(tree) else '0'
            print(line)
            line = ''

    def print_scores(self):
        line = ''
        for j in range(self.h):
            for i in range(self.w):
                tree = self.get_tree(i, j)
                line += str(self.tree_score(tree))
            print(line)
            line = ''

class Tree:
    def __init__(self, x, y, h) -> None:
        self.x = x
        self.y = y
        self.h = int(h)

    @property
    def pos(self):
        return (self.x, self.y)
    
    def __str__(self) -> str:
        return '({}, {}) -> {}'.format(self.x, self.y, self.h)
    
    def __repr__(self) -> str:
        return str(self)


class Y2022D08Solver(BaseSolver):
    def solve_part_a(self):
        grid = Grid(len(self.lines[0]), len(self.lines))

        for j, line in enumerate(self.lines):
            for i, h in enumerate(line):
                tree = Tree(i, j, h)
                grid.add_tree(tree)
        
        return grid.visible_trees_count()
    

    def solve_part_b(self):
        grid = Grid(len(self.lines[0]), len(self.lines))

        for j, line in enumerate(self.lines):
            for i, h in enumerate(line):
                tree = Tree(i, j, h)
                grid.add_tree(tree)
        
        max_tree_score = 0
        for tree in grid.trees.values():
            tree_score = grid.tree_score(tree)
            if tree_score > max_tree_score:
                max_tree_score = tree_score
        
        return max_tree_score
