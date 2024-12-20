from __future__ import annotations

from functools import cache

from util import Day


class Day19Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(19, part1_expect, part2_expect, example)
        self.towels = self.lines[0].split(", ")
        self.patterns_wanted = self.lines[2:]

    @cache
    def can_continue_pattern(self, pattern: str) -> bool:
        if pattern == "":
            return True

        for towel in self.towels:
            if pattern.startswith(towel) and self.can_continue_pattern(pattern[len(towel):]):
                return True

        return False

    @cache
    def pattern_possibilities(self, pattern: str) -> int:
        if pattern == "":
            return 1

        count = 0
        for towel in self.towels:
            if pattern.startswith(towel):
                count +=  self.pattern_possibilities(pattern[len(towel):])

        return count

    def part1(self) -> int:
        possible = 0
        for pattern in self.patterns_wanted:
            if self.can_continue_pattern(pattern):
                possible += 1

        return possible

    def part2(self) -> int:
        possible = 0
        for pattern in self.patterns_wanted:
            possible += self.pattern_possibilities(pattern)

        return possible

class Day19Example(Day19Base):
    def __init__(self) -> None:
        super().__init__(6, 16, True)

class Day19(Day19Base):
    def __init__(self) -> None:
        super().__init__(300, 624802218898092, False)

if __name__ == "__main__":
    Day19Example().check()
    Day19().check()
