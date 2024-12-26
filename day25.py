from __future__ import annotations

from util import Day


def pivot(strings: list[str]) -> list[str]:
    result: list[str] = ["", "", "", "", ""]
    for column in range(len(strings)):
        for row in range(len(strings[0])):
            result[row] += strings[column][row]
    return result

class Day25Base(Day):
    def __init__(
        self,
        part1_expect: str | int | None,
        part2_expect: str | int | None,
        example: bool,
    ) -> None:
        super().__init__(25, part1_expect, part2_expect, example)
        self.locks: list[list[int]] = []
        self.keys: list[list[int]] = []

        for item in self.text.split("\n\n"):
            lines = item.splitlines()
            if lines[0] == "#####":
                lines.pop(0)
                item_type = "lock"
            else:
                item_type = "key"
                lines.pop()

            as_numbers = [string.count("#") for string in pivot(lines)]

            if item_type == "lock":
                self.locks.append(as_numbers)
            else:
                self.keys.append(as_numbers)

    def part1(self) -> int:
        pairs_that_fit = 0

        for lock in self.locks:
            for key in self.keys:
                fit = True
                for index in range(len(key)):
                    if lock[index] > (5 - key[index]):
                        fit = False
                        break

                if fit:
                    pairs_that_fit += 1

        return pairs_that_fit

    def part2(self) -> int:
        return 0

class Day25Example(Day25Base):
    def __init__(self) -> None:
        super().__init__(3, None, True)

class Day25(Day25Base):
    def __init__(self) -> None:
        super().__init__(3065, None, False)

if __name__ == "__main__":
    # Day25Example().check()
    Day25().check()
