import math

from advent_of_code.basesolver import BaseSolver


class Y2020D13Solver(BaseSolver):
    def solve_part_a(self):
        my_time = int(self.lines[0])
        bus_ids = [int(id) for id in self.lines[1].split(",") if id != "x"]

        min_diff = float("inf")
        min_diff_id = None

        for bus_id in bus_ids:
            closest_time = math.ceil(my_time / bus_id) * bus_id
            diff = closest_time - my_time
            if diff < min_diff:
                min_diff = diff
                min_diff_id = bus_id

        return str(min_diff_id * min_diff)

    def solve_part_b(self):
        bus_ids = self.lines[1].split(",")
        minutes_after_start_id = {}
        for index, bus_id in enumerate(bus_ids, 0):
            if bus_id != "x":
                minutes_after_start_id[int(bus_id)] = index

        eqs = []
        for bus_id, minutes_after in minutes_after_start_id.items():
            right_b = bus_id - minutes_after
            while right_b >= bus_id or right_b < 0:
                if right_b >= bus_id:
                    right_b -= bus_id
                elif right_b < 0:
                    right_b += bus_id

            eqs.append({"mod_by": bus_id, "b": right_b})

        """
        eqs = [
            {'mod_by': 5, 'b': 3},
            {'mod_by': 7, 'b': 1},
            {'mod_by': 8, 'b': 6},
        ]
        """
        prod = 1
        for eq in eqs:
            prod *= eq["mod_by"]
        N = int(prod)

        for eq in eqs:
            eq["N"] = N // eq["mod_by"]

        for eq in eqs:
            lowest_N = eq["N"]
            if eq["N"] > eq["mod_by"]:
                lowest_N = eq["N"] - (math.floor(eq["N"] / eq["mod_by"]) * eq["mod_by"])

            x = 1
            while True:
                if (lowest_N * x) % eq["mod_by"] == 1:
                    break
                x += 1

            eq["x"] = x

        for eq in eqs:
            eq["prod"] = eq["b"] * eq["N"] * eq["x"]

        result = sum([eq["prod"] for eq in eqs])
        lowest_result = result
        if result > N:
            lowest_result = result - (math.floor(result / N) * N)

        return str(int(lowest_result))
