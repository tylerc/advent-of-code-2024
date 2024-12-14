from __future__ import annotations

from dataclasses import dataclass

from util import Day

OPS = ["+", "*"]

@dataclass
class Equation:
    result: int
    numbers: list[int]

    def evaluation_valid(self, ops: list[str]) -> bool:
        if len(self.numbers) == 1:
            return self.numbers[0] == self.result

        for op in ops:
            nums_next = self.numbers[:]
            left = nums_next.pop(0)
            right = nums_next.pop(0)
            if op == "+":
                nums_next.insert(0, left + right)
                if Equation(result=self.result, numbers=nums_next).evaluation_valid(ops):
                    return True
            elif op == "*":
                nums_next.insert(0, left * right)
                if Equation(result=self.result, numbers=nums_next).evaluation_valid(ops):
                    return True
            elif op == "||":
                nums_next.insert(0, int(str(left) + str(right)))
                if Equation(result=self.result, numbers=nums_next).evaluation_valid(ops):
                    return True

        return False

class Day07Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(7, part1_expect, part2_expect, example)

        self.equations: list[Equation] = []
        for line in self.lines:
            (result, remaining) = line.split(": ")
            numbers = [int(num) for num in remaining.split(" ")]
            self.equations.append(Equation(int(result), numbers))

    def part1(self) -> int:
        result = 0

        for equation in self.equations:
            if equation.evaluation_valid(ops=["+", "*"]):
                result += equation.result

        return result

    def part2(self) -> int:
        result = 0

        for equation in self.equations:
            if equation.evaluation_valid(ops=["+", "*", "||"]):
                result += equation.result

        return result

class Day07Example(Day07Base):
    def __init__(self) -> None:
        super().__init__(3749, 11387, True)

class Day07(Day07Base):
    def __init__(self) -> None:
        super().__init__(882304362421, 145149066755184, False)

if __name__ == "__main__":
    # Day07Example().check()
    Day07().check()
