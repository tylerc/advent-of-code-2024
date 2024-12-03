import re

from util import Day


class Day03(Day):
    def __init__(self) -> None:
        super().__init__(3, 174960292, 56275602)

    def part1(self) -> int:
        total = 0

        for match in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", self.text):
            total += int(match[0]) * int(match[1])

        return total

    def part2(self) -> int:
        total = 0
        enabled = True

        for match in re.findall(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))", self.text):
            if match[0] == "do()":
                enabled = True
            elif match[0] == "don't()":
                enabled = False
            elif enabled:
                total += int(match[1]) * int(match[2])

        return total

if __name__ == "__main__":
    Day03().check()
