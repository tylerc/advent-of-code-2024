from __future__ import annotations

from collections import Counter

from util import Day


class Day20Base(Day):
    def __init__(
        self,
        part1_expect: str | int | None,
        part2_expect: str | int | None,
        example: bool,
    ) -> None:
        super().__init__(20, part1_expect, part2_expect, example)
        self.walls: set[tuple[int, int]] = set()
        self.start = (-1, -1)
        self.end = (-1, -1)
        self.width = len(self.lines[0])
        self.height = len(self.lines)

        for y in range(self.height):
            for x in range(self.width):
                char = self.lines[y][x]
                if char == "#":
                    self.walls.add((x, y))
                elif char == "S":
                    self.start = (x, y)
                elif char == "E":
                    self.end = (x, y)

        self.cheats_part_1: set[tuple[tuple[int, int], tuple[int, int]]] = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for y in range(len(self.lines)):
            for x in range(len(self.lines[0])):
                pos = (x, y)
                if pos in self.walls:
                    continue

                for direction in directions:
                    end_pos = (pos[0] + direction[0] * 2, pos[1] + direction[1] * 2)
                    if 0 <= end_pos[0] < self.width and 0 <= end_pos[1] < self.height and end_pos not in self.walls:
                        self.cheats_part_1.add((pos, end_pos))

        self.cheats_part_2: set[tuple[tuple[int, int], tuple[int, int]]] = set()
        for y in range(len(self.lines)):
            for x in range(len(self.lines[0])):
                pos = (x, y)
                if pos in self.walls:
                    continue

                for x_diff in range(-20, 21):
                    for y_diff in range(-20, 21):
                        total_diff = abs(x_diff) + abs(y_diff)
                        if total_diff > 20 or total_diff == 0:
                            continue
                        end_pos = (x + x_diff, y + y_diff)
                        if 0 <= end_pos[0] < self.width and 0 <= end_pos[1] < self.height and end_pos not in self.walls:
                            self.cheats_part_2.add((pos, end_pos))

    def compute_distances_from_start(self, occupied: set[tuple[int, int]]) -> dict[tuple[int, int], int]:
        to_visit = [(self.start, 0)]
        visited: dict[tuple[int, int], int] = {}
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while len(to_visit) > 0:
            pos, cost = to_visit.pop()
            cost_existing = visited.get(pos)
            if cost_existing is not None and cost >= cost_existing:
                continue
            visited[pos] = cost

            for diff in directions:
                new_pos = (pos[0] + diff[0], pos[1] + diff[1])
                if new_pos not in occupied and 0 <= new_pos[0] <= self.width and 0 <= new_pos[1] <= self.height:
                    to_visit.append((new_pos, cost + 1))

        return visited

    def count_cheats(self, cheats: set[tuple[tuple[int, int], tuple[int, int]]]) -> Counter[int]:
        distances = self.compute_distances_from_start(self.walls)
        counter: Counter[int] = Counter()

        for cheat in cheats:
            start_distance = distances[cheat[0]]
            end_distance = distances[cheat[1]]
            if end_distance <= start_distance:
                continue
            diff = end_distance - start_distance - (abs(cheat[0][0] - cheat[1][0]) + abs(cheat[0][1] - cheat[1][1]))
            if diff > 0:
                counter[diff] += 1

        return counter

    def part1(self) -> int:
        return sum(cheats for picoseconds, cheats in self.count_cheats(self.cheats_part_1).items() if picoseconds >= 100)

    def part2(self) -> int:
        return sum([cheats for picoseconds, cheats in self.count_cheats(self.cheats_part_2).items() if picoseconds >= 100])

class Day20Example(Day20Base):
    def __init__(self) -> None:
        super().__init__(0, None, True)

class Day20(Day20Base):
    def __init__(self) -> None:
        super().__init__(1367, 1006850, False)

if __name__ == "__main__":
    # Day20Example().check()
    Day20().check()
