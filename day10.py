from collections.abc import Iterator

from util import Day


class Day10Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(10, part1_expect, part2_expect, example)

        self.grid: dict[tuple[int, int], int] = {}
        self.width = len(self.lines[0])
        self.height = len(self.lines)
        self.starts: list[tuple[int, int]] = []

        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                num = int(char)
                self.grid[(x, y)] = num

                if num == 0:
                    self.starts.append((x, y))

    def surrounding_positions(self, pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        for diff in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = pos[0] + diff[0], pos[1] + diff[1]
            if 0 <= new_pos[0] < self.width and 0 <= new_pos[1] < self.height:
                yield new_pos

    def hikeable_positions(self, pos: tuple[int, int], visited: set[tuple[int, int]]) -> Iterator[tuple[int, int]]:
        grade = self.grid[pos]
        for other_pos in self.surrounding_positions(pos):
            other_grade = self.grid[other_pos]
            if other_grade - grade == 1 and other_pos not in visited:
                yield other_pos

    def nines_reachable(self, start: tuple[int, int]) -> Iterator[tuple[int, int]]:
        to_visit: list[tuple[tuple[int, int], set[tuple[int, int]]]] = [(start, {start})]

        while len(to_visit) > 0:
            pos, visited = to_visit.pop()
            grade = self.grid[pos]
            if grade == 9:
                yield pos

            for new_pos in self.hikeable_positions(pos, visited):
                new_visited = set(visited)
                new_visited.add(new_pos)
                to_visit.append((new_pos, new_visited))

    def part1(self) -> int:
        result = 0

        for start in self.starts:
            result += len(set(self.nines_reachable(start)))

        return result

    def part2(self) -> int:
        result = 0

        for start in self.starts:
            result += sum(1 for _ in self.nines_reachable(start))

        return result

class Day10Example(Day10Base):
    def __init__(self) -> None:
        super().__init__(36, 81, True)

class Day10(Day10Base):
    def __init__(self) -> None:
        super().__init__(778, 1925, False)

if __name__ == "__main__":
    # Day10Example().check()
    Day10().check()
