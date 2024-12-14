import re
from dataclasses import dataclass

from util import Day


@dataclass
class Prize:
    button_a_x: int
    button_a_y: int
    button_b_x: int
    button_b_y: int
    prize_x: int
    prize_y: int

    # Based on the problem statement, we know the resulting prize x/y positions can be described by the following
    # equations:
    #   prize_x = button_a_x * a_presses + button_b_x * b_presses
    #.  prize_y = button_a_y * a_presses + button_b_y * b_presses
    #
    # We can solve both of these for the number of presses:
    #   a_presses = (prize_x - button_b_x * b_presses)/button_a_x
    #   b_presses = (prize_y - button_a_y * a_presses)/button_b_y
    #
    # By combining the two equations and solving for a_presses, we create this equation for a_presses which is
    # composed entirely of constants, and can be evaluated directly:
    #   a_presses = (prize_x - (button_b_x * prize_y)/button_b_y)/(button_a_x - (button_b_x * button_a_y)/button_b_y)
    #
    # b_presses can then be found by plugging a_presses into the simpler equation mentioned previously.
    #
    # Because partial button presses aren't allowed, and because of floating point imprecision, we round our answers
    # and then check them against our initial equations for prize_x and prize_y to determine if we found a workable
    # solution.
    def victory_condition(self) -> None | tuple[int, int, int]:
        a_presses_float = (self.prize_x - (self.button_b_x * self.prize_y)/self.button_b_y)/(self.button_a_x - (self.button_b_x * self.button_a_y)/self.button_b_y)
        b_presses_float = (self.prize_y - self.button_a_y * a_presses_float)/self.button_b_y

        a_presses = round(a_presses_float)
        b_presses = round(b_presses_float)
        if (a_presses * self.button_a_x) + (b_presses * self.button_b_x) != self.prize_x:
            return None
        if (a_presses * self.button_a_y) + (b_presses * self.button_b_y) != self.prize_y:
            return None

        return a_presses * 3 + b_presses, a_presses, b_presses

class Day13Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(13, part1_expect, part2_expect, example)
        self.prizes: list[Prize] = []
        for i in range(0, len(self.lines), 4):
            button_a = re.match(r"Button A: X\+(\d+), Y\+(\d+)", self.lines[i])
            button_b = re.match(r"Button B: X\+(\d+), Y\+(\d+)", self.lines[i + 1])
            prize = re.match(r"Prize: X=(\d+), Y=(\d+)", self.lines[i + 2])
            assert isinstance(button_a, re.Match)
            assert isinstance(button_b, re.Match)
            assert isinstance(prize, re.Match)
            self.prizes.append(Prize(
                button_a_x=int(button_a[1]),
                button_a_y=int(button_a[2]),
                button_b_x=int(button_b[1]),
                button_b_y=int(button_b[2]),
                prize_x=int(prize[1]),
                prize_y=int(prize[2]),
            ))

    def part1(self) -> int:
        token_cost = 0

        for prize in self.prizes:
            victory = prize.victory_condition()
            if victory:
                token_cost += victory[0]

        return token_cost

    def part2(self) -> int:
        token_cost = 0

        for prize in self.prizes:
            prize.prize_x += 10000000000000
            prize.prize_y += 10000000000000
            victory = prize.victory_condition()
            if victory:
                token_cost += victory[0]

        return token_cost

class Day13Example(Day13Base):
    def __init__(self) -> None:
        super().__init__(480, None, True)

class Day13(Day13Base):
    def __init__(self) -> None:
        super().__init__(36954, 79352015273424, False)

if __name__ == "__main__":
    Day13Example().check()
    Day13().check()
