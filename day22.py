from __future__ import annotations

from collections import Counter
from collections.abc import Iterator

from util import Day


def evolve_n(secret: int, iters: int) -> Iterator[int]:
    for _ in range(iters):
        secret = evolve(secret)
        yield secret

def evolve(secret: int) -> int:
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret

def mix(secret: int, mixing: int) -> int:
    return secret ^ mixing

def prune(secret: int) -> int:
    return secret % 16777216

class Day22Base(Day):
    def __init__(
        self,
        part1_expect: str | int | None,
        part2_expect: str | int | None,
        example: bool,
    ) -> None:
        super().__init__(22, part1_expect, part2_expect, example)
        self.starts = [int(line) for line in self.lines]

    def part1(self) -> int:
        result = 0

        for num in self.starts:
            *_, last = evolve_n(num, 2000)
            result += last

        return result

    def part2(self) -> int:
        bananas_by_sequence: Counter[tuple[int, int, int, int]] = Counter()

        for start in self.starts:
            bananas_history: list[int] = [start % 10]
            diffs: list[int] = []
            sequences_seen: set[tuple[int, int, int, int]] = set()

            for num in evolve_n(start, 2000):
                bananas = num % 10
                bananas_last = bananas_history[-1]
                diffs.append(bananas - bananas_last)
                bananas_history.append(bananas)

                if len(diffs) >= 4:
                    sequence = (diffs[-4], diffs[-3], diffs[-2], diffs[-1])
                    if sequence in sequences_seen:
                        continue
                    sequences_seen.add(sequence)
                    bananas_by_sequence[sequence] += bananas

        return bananas_by_sequence.most_common()[0][1]

class Day22Example(Day22Base):
    def __init__(self) -> None:
        super().__init__(None, None, True)

class Day22(Day22Base):
    def __init__(self) -> None:
        super().__init__(17965282217, 2152, False)

if __name__ == "__main__":
    # Day22Example().check()
    Day22().check()
