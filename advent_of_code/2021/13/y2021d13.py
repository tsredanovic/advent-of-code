from advent_of_code.basesolver import BaseSolver

class Paper:
    def __init__(self, lines) -> None:
        self.pos_list = []
        for line in lines:
            x, y = line.split(',')
            self.pos_list.append((int(x), int(y)))
        
        self._width = None
        self._height = None

    def calculate_wh(self):
        max_x = 0
        max_y = 0
        for pos in self.pos_list:
            if pos[0] > max_x:
                max_x = pos[0]
            if pos[1] > max_y:
                max_y = pos[1]
        
        self._width = max_x + 1
        self._height = max_y + 1

    @property
    def width(self):
        if not self._width:
            self.calculate_wh()
        return self._width

    @property
    def height(self):
        if not self._height:
            self.calculate_wh()
        return self._height
    
    def count_dots(self):
        dots_count = 0
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) not in self.pos_list:
                    dots_count += 1
        return dots_count

    def __str__(self) -> str:
        paper_str = ''
        for y in range(self.height):
            for x in range(self.width):
                paper_str += '#' if (x,y) in self.pos_list else '.'
            paper_str += '\n'
        return paper_str.strip()

    def __repr__(self) -> str:
        return str(self)

    def horizontal_fold(self, fold_at_y):
        # get everything under fold_at_y
        positions_to_fold = []
        for pos in self.pos_list:
            if pos[1] > fold_at_y:
                positions_to_fold.append(pos)
        # fold those positions
        folded_positions = []
        for pos in positions_to_fold:
            y_offset = pos[1] - fold_at_y
            new_y = fold_at_y - y_offset
            folded_positions.append((pos[0], new_y))
        # folded paper positions
        folded_paper_positions = []
        for pos in self.pos_list:
            if pos[1] < fold_at_y:
                folded_paper_positions.append(pos)
        for pos in folded_positions:
            if pos not in folded_paper_positions:
                folded_paper_positions.append(pos)
        # folded paper
        folded_paper = Paper([])
        folded_paper.pos_list = folded_paper_positions
        folded_paper._height = fold_at_y
        folded_paper._width = self.width
        return folded_paper

    def vertical_fold(self, fold_at_x):
        # get everything right from fold_at_x
        positions_to_fold = []
        for pos in self.pos_list:
            if pos[0] > fold_at_x:
                positions_to_fold.append(pos)
        # fold those positions
        folded_positions = []
        for pos in positions_to_fold:
            x_offset = pos[0] - fold_at_x
            new_x = fold_at_x - x_offset
            folded_positions.append((new_x, pos[1]))
        # folded paper positions
        folded_paper_positions = []
        for pos in self.pos_list:
            if pos[0] < fold_at_x:
                folded_paper_positions.append(pos)
        for pos in folded_positions:
            if pos not in folded_paper_positions:
                folded_paper_positions.append(pos)
        # folded paper
        folded_paper = Paper([])
        folded_paper.pos_list = folded_paper_positions
        folded_paper._height = self._height
        folded_paper._width = fold_at_x
        return folded_paper


class Y2021D13Solver(BaseSolver):
    def solve_part_a(self):
        paper_lines = []
        fold_lines = []
        is_paper_lines = True
        for line in self.lines:
            if line == '':
                is_paper_lines = False
                continue
            if is_paper_lines:
                paper_lines.append(line)
            else:
                fold_lines.append(line)
        current_paper = Paper(paper_lines)
        #print('Initial paper:')
        #print(current_paper)
        
        for fold_line in fold_lines[:1]:
            #print(fold_line)
            x_or_y = fold_line.split()[-1].split('=')[0]
            fold_at = int(fold_line.split()[-1].split('=')[1])
            if x_or_y == 'y':
                current_paper = current_paper.horizontal_fold(fold_at)
            else:
                current_paper = current_paper.vertical_fold(fold_at)
            #print(current_paper)
        
        return len(current_paper.pos_list)

    def solve_part_b(self):
        paper_lines = []
        fold_lines = []
        is_paper_lines = True
        for line in self.lines:
            if line == '':
                is_paper_lines = False
                continue
            if is_paper_lines:
                paper_lines.append(line)
            else:
                fold_lines.append(line)
        current_paper = Paper(paper_lines)
        #print('Initial paper:')
        #print(current_paper)
        
        for fold_line in fold_lines:
            #print(fold_line)
            x_or_y = fold_line.split()[-1].split('=')[0]
            fold_at = int(fold_line.split()[-1].split('=')[1])
            if x_or_y == 'y':
                current_paper = current_paper.horizontal_fold(fold_at)
            else:
                current_paper = current_paper.vertical_fold(fold_at)
            #print(current_paper)
        
        return '\n' + str(current_paper)

