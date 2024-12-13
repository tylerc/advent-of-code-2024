from collections.abc import Iterator
from functools import cache

from util import Day


class Day11Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(11, part1_expect, part2_expect, example)
        self.stones: list[int] = []
        for num in self.lines[0].split(" "):
            self.stones.append(int(num))

    @staticmethod
    def produce_next(stones: list[int]) -> Iterator[int]:
        for stone in stones:
            if stone == 0:
                yield 1
                continue
            num_str = str(stone)
            if len(num_str) % 2 == 0:
                midpoint = int(len(num_str) / 2)
                yield int(num_str[:midpoint])
                yield int(num_str[midpoint:])
            else:
                yield stone * 2024

    @staticmethod
    @cache
    def stone_number_to_count(stone: int, iters: int) -> int:
        if iters == 0:
            return 1

        stones_next = list(Day11Base.produce_next([stone]))
        return sum([Day11Base.stone_number_to_count(s, iters - 1) for s in stones_next])

    def part1(self) -> int:
        return sum([Day11Base.stone_number_to_count(s, 25) for s in self.stones])

    def part2(self) -> int:
        return sum([Day11Base.stone_number_to_count(s, 75) for s in self.stones])

class Day11Example(Day11Base):
    def __init__(self) -> None:
        super().__init__(55312, None, True)

class Day11(Day11Base):
    def __init__(self) -> None:
        super().__init__(193899, 229682160383225, False)

if __name__ == "__main__":
    # Day11Example().check()
    Day11().check()
