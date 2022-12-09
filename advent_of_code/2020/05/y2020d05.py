import itertools

from advent_of_code.basesolver import BaseSolver


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]


class Seat:
    def __init__(self, spec=None, row=None, col=None):
        self.spec = spec
        self.row = row if row is not None else self.find_row(spec)
        self.col = col if col is not None else self.find_col(spec)
        self.id = self.row * 8 + self.col

    def find_row(self, spec):
        row_spec = spec[0:7]

        current_rows = [row for row in range(0, 128)]
        for char in row_spec:
            lower_rows, upper_rows = split_list(current_rows)
            if char == "F":
                current_rows = lower_rows
            elif char == "B":
                current_rows = upper_rows

        return current_rows[0]

    def find_col(self, spec):
        col_spec = spec[7:]

        current_cols = [row for row in range(0, 8)]
        for char in col_spec:
            lower_cols, upper_cols = split_list(current_cols)
            if char == "L":
                current_cols = lower_cols
            elif char == "R":
                current_cols = upper_cols

        return current_cols[0]

    def __str__(self):
        return "row {}, column {}, seat ID {}".format(self.row, self.col, self.id)

    def __repr__(self):
        return self.__str__()


class Y2020D05Solver(BaseSolver):
    def solve_part_a(self):
        seat_ids = []
        for spec in self.lines:
            seat = Seat(spec)
            seat_ids.append(seat.id)

        return str(max(seat_ids))

    def solve_part_b(self):
        # List seats
        list_seats = []
        for spec in self.lines:
            list_seats.append(Seat(spec))

        # All seats
        all_rows = [row for row in range(0, 128)]
        all_cols = [row for row in range(0, 8)]
        all_seats = []
        for row_col in itertools.product(all_rows, all_cols):
            row = row_col[0]
            col = row_col[1]
            seat = Seat(row=row, col=col)
            all_seats.append(seat)

        # Empty seats
        empty_seats = []
        for seat in all_seats:
            is_empty = True
            seat_id = seat.id
            for list_seat in list_seats:
                list_site_id = list_seat.id
                if list_site_id == seat_id:
                    is_empty = False
                    continue
            if is_empty:
                empty_seats.append(seat)

        # Filter empty seats
        current_min_id = 0
        for seat in empty_seats:
            if seat.id != current_min_id:
                return str(seat.id)
            current_min_id += 1
