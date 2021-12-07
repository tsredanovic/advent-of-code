
import pprint

from basesolver import BaseSolver

class Board:
    def __init__(self, lines) -> None:
        for i in range(len(lines)):
            lines[i] = lines[i].strip()

        number_lines = []
        for line in lines:
            number_lines.append([int(num) for num in line.split()])
        self.number_lines = number_lines

        self.numbers_dict = {}
        self.positions_dict = {}
        for i in range(len(self.number_lines)):
            for j in range(len(self.number_lines[0])):
                number = self.number_lines[i][j]
                self.numbers_dict[number] = (i, j)
                self.positions_dict[(i, j)] = number

        self.marked_positions = []

        win_positions = []
        for i in range(len(self.number_lines)):
            win_row_positions = []
            win_col_positions = []
            for j in range(len(self.number_lines[0])):
                win_row_positions.append((i, j))
                win_col_positions.append((j, i))
            win_positions.append(win_row_positions)
            win_positions.append(win_col_positions)
        
        self.win_positions = win_positions

    def __str__(self) -> str:
        return pprint.pformat(self.number_lines)
    
    def __repr__(self) -> str:
        return str(self)
    
    def mark_position(self, number) -> bool:
        if not self.numbers_dict.get(number):
            return False
        if self.numbers_dict.get(number) in self.marked_positions:
            return True
        self.marked_positions.append(self.numbers_dict[number])
        return True
    
    def check_win(self):
        if len(self.marked_positions) < 5:
            return False, None

        for win_position in self.win_positions:
            if len(set(win_position).intersection(set(self.marked_positions))) == 5:
                return True, win_position

        return False, None
    
    def unmarked_sum(self):
        score = 0
        for i in range(len(self.number_lines)):
            for j in range(len(self.number_lines[0])):
                if (i, j) not in self.marked_positions:
                    number = self.number_lines[i][j]
                    score += number
        return score
    
    def draws_to_win(self, drawn_numbers):
        for drawn_number_i, drawn_num in enumerate(drawn_numbers):
            number_marked = self.mark_position(drawn_num)
            if number_marked:
                won, win_position = self.check_win()
                if won:
                    return drawn_number_i, drawn_num

def generate_boards(lines):
    if not lines[0]:
        lines = lines[1:]
    if lines[-1]:
        lines.append('')
    all_boards_lines = []
    current_board_lines = []
    for line in lines:
        if not line:
            all_boards_lines.append(current_board_lines)
            current_board_lines = []
        else:
            current_board_lines.append(line)
    
    boards = []
    for board_lines in all_boards_lines:
        boards.append(Board(board_lines))

    return boards

class Y2021D04Solver(BaseSolver):
    def solve_part_a(self):
        drawn_numbers = [int(num) for num in self.lines[0].split(',')]
        boards = generate_boards(self.lines[2:])

        for drawn_num in drawn_numbers:
            for board in boards:
                number_marked = board.mark_position(drawn_num)
                if number_marked:
                    won, win_position = board.check_win()
                    if won:
                        return board.unmarked_sum() * drawn_num
    

    def solve_part_b(self):
        drawn_numbers = [int(num) for num in self.lines[0].split(',')]
        boards = generate_boards(self.lines[2:])

        high_draws_to_win = -1
        high_draws_to_win_board_i = -1
        high_draws_to_win_number = -1
        for board_i, board in enumerate(boards):
            draws_to_win, won_on_number = board.draws_to_win(drawn_numbers)
            if draws_to_win > high_draws_to_win:
                high_draws_to_win = draws_to_win
                high_draws_to_win_board_i = board_i
                high_draws_to_win_number = won_on_number
        high_draws_to_win_board = boards[high_draws_to_win_board_i]
        return high_draws_to_win_board.unmarked_sum() * high_draws_to_win_number


