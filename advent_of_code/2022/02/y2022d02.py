from advent_of_code.basesolver import BaseSolver


class RoundA:
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    OPP_MAP = {
        "A": ROCK,
        "B": PAPER,
        "C": SCISSORS,
    }
    ME_MAP = {
        "X": ROCK,
        "Y": PAPER,
        "Z": SCISSORS,
    }

    ME_WIN = "me_win"
    OPP_WIN = "opp_win"
    DRAW = "draw"

    OUTCOMES = {
        # (opp_move, me_move)
        (ROCK, ROCK): DRAW,
        (ROCK, PAPER): ME_WIN,
        (ROCK, SCISSORS): OPP_WIN,
        (PAPER, ROCK): OPP_WIN,
        (PAPER, PAPER): DRAW,
        (PAPER, SCISSORS): ME_WIN,
        (SCISSORS, ROCK): ME_WIN,
        (SCISSORS, PAPER): OPP_WIN,
        (SCISSORS, SCISSORS): DRAW,
    }

    MOVE_SCORE = {
        ROCK: 1,
        PAPER: 2,
        SCISSORS: 3,
    }
    OUTCOME_SCORE = {
        OPP_WIN: 0,
        DRAW: 3,
        ME_WIN: 6,
    }

    def __init__(self, line) -> None:
        self.opp_code = line.split(" ")[0]
        self.me_code = line.split(" ")[1]

        self.opp_move = self.OPP_MAP[self.opp_code]
        self.me_move = self.ME_MAP[self.me_code]

        self.outcome = self.OUTCOMES[(self.opp_move, self.me_move)]

        self.move_score = self.MOVE_SCORE[self.me_move]
        self.outcome_score = self.OUTCOME_SCORE[self.outcome]
        self.score = self.move_score + self.outcome_score

    def __str__(self) -> str:
        return "{} (OPP) vs {} (ME) -> {} | Score: {}".format(
            self.opp_move, self.me_move, self.outcome, self.score
        )

    def __repr__(self) -> str:
        return str(self)


class RoundB:
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    ME_WIN = "me_win"
    OPP_WIN = "opp_win"
    DRAW = "draw"

    OPP_MAP = {
        "A": ROCK,
        "B": PAPER,
        "C": SCISSORS,
    }
    OUTCOME_MAP = {
        "X": OPP_WIN,
        "Y": DRAW,
        "Z": ME_WIN,
    }

    ME_MOVES = {
        # (opp_move, me_move)
        (ROCK, OPP_WIN): SCISSORS,
        (ROCK, DRAW): ROCK,
        (ROCK, ME_WIN): PAPER,
        (PAPER, OPP_WIN): ROCK,
        (PAPER, DRAW): PAPER,
        (PAPER, ME_WIN): SCISSORS,
        (SCISSORS, OPP_WIN): PAPER,
        (SCISSORS, DRAW): SCISSORS,
        (SCISSORS, ME_WIN): ROCK,
    }

    MOVE_SCORE = {
        ROCK: 1,
        PAPER: 2,
        SCISSORS: 3,
    }
    OUTCOME_SCORE = {
        OPP_WIN: 0,
        DRAW: 3,
        ME_WIN: 6,
    }

    def __init__(self, line) -> None:
        self.opp_code = line.split(" ")[0]
        self.outcome_code = line.split(" ")[1]

        self.opp_move = self.OPP_MAP[self.opp_code]
        self.outcome = self.OUTCOME_MAP[self.outcome_code]

        self.me_move = self.ME_MOVES[(self.opp_move, self.outcome)]

        self.move_score = self.MOVE_SCORE[self.me_move]
        self.outcome_score = self.OUTCOME_SCORE[self.outcome]
        self.score = self.move_score + self.outcome_score

    def __str__(self) -> str:
        return "{} (OPP) vs {} (ME) -> {} | Score: {}".format(
            self.opp_move, self.me_move, self.outcome, self.score
        )

    def __repr__(self) -> str:
        return str(self)


class Y2022D02Solver(BaseSolver):
    def solve_part_a(self):
        total_score = 0
        for line in self.lines:
            round = RoundA(line)
            total_score += round.score
        return total_score

    def solve_part_b(self):
        total_score = 0
        for line in self.lines:
            round = RoundB(line)
            total_score += round.score
        return total_score
