from dataclasses import dataclass
from math import floor

from util import Day


@dataclass
class Rule:
    before: int
    after: int

class Day05Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(5, part1_expect, part2_expect, example)
        empty_index = self.lines.index("")
        self.rules = [Rule(*[int(s) for s in line.split("|")]) for line in self.lines[:empty_index]]
        self.sequences = [[int(s) for s in line.split(",")] for line in self.lines[empty_index + 1:]]
        self.sequences_valid: list[list[int]] = []
        self.sequences_invalid: list[list[int]] = []
        for sequence in self.sequences:
            if self.sequence_is_valid(sequence):
                self.sequences_valid.append(sequence)
            else:
                self.sequences_invalid.append(sequence)

        self.value_and_direct_followers: dict[int, set[int]] = {}
        for rule in self.rules:
            self.value_and_direct_followers.setdefault(rule.before, set()).add(rule.after)

    def collect_transitive_followers(
            self,
            applicable: set[int],
            value: int,
            visited: set[int],
    ) -> set[int]:
        direct_followers = self.value_and_direct_followers.get(value, set()).intersection(applicable)
        to_visit = set(direct_followers)
        while len(to_visit) > 0:
            visiting_next = to_visit.pop()
            if visiting_next not in visited:
                visited.add(visiting_next)
                self.collect_transitive_followers(applicable, visiting_next, visited)

        return visited

    def count_transitive_followers(self, applicable: set[int]) -> dict[int, int]:
        transitive_followers: dict[int, set[int]] = {}
        for value in applicable:
            transitive_followers[value] = self.collect_transitive_followers(applicable, value, {value})
        return {value: len(followers) for value, followers in transitive_followers.items()}

    def sequence_is_valid(self, sequence: list[int]) -> bool:
        for index, item in enumerate(sequence):
            before = sequence[:index]
            after = sequence[index + 1:]
            if not self.obeys_rules(item, before, after):
                return False

        return True

    def obeys_rules(self, item: int, before: list[int], after: list[int]) -> bool:
        for rule in self.rules:
            for other in before:
                if rule.before == item and rule.after == other:
                    return False
            for other in after:
                if rule.after == item and rule.before == other:
                    return False

        return True

    def part1(self) -> int:
        result = 0
        for sequence in self.sequences_valid:
            result += sequence[floor(len(sequence) / 2)]

        return result

    def part2(self) -> int:
        result = 0
        for sequence in self.sequences_invalid:
            counts = self.count_transitive_followers(set(sequence))
            fixed = sorted(sequence, key=lambda item: counts.get(item, 0), reverse=True)
            result += fixed[floor(len(fixed) / 2)]

        return result

class Day05Example(Day05Base):
    def __init__(self) -> None:
        super().__init__(143, 123, True)

class Day05(Day05Base):
    def __init__(self) -> None:
        super().__init__(3608, 4922, False)

if __name__ == "__main__":
    # Day05Example().check()
    Day05().check()
