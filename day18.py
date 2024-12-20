from __future__ import annotations

from util import Day


class Day18Base(Day):
    def __init__(
            self,
            part1_steps: int,
            end: tuple[int, int],
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(18, part1_expect, part2_expect, example)
        self.part1_steps = part1_steps
        self.end = end
        self.bytes: list[tuple[int, int]] = []
        for line in self.lines:
            left, right = line.split(",")
            self.bytes.append((int(left), int(right)))

    def find_shortest_path(self, occupied: set[tuple[int, int]]) -> int:
        to_visit = [((0, 0), 0)]
        visited: dict[tuple[int, int], int] = {}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while len(to_visit) > 0:
            pos, cost = to_visit.pop(0)
            cost_existing = visited.get(pos)
            if cost_existing and cost >= cost_existing:
                continue
            visited[pos] = cost

            for diff in directions:
                new_pos = (pos[0] + diff[0], pos[1] + diff[1])
                if new_pos not in occupied and 0 <= new_pos[0] <= self.end[0] and 0 <= new_pos[1] <= self.end[1]:
                    to_visit.append((new_pos, cost + 1))

        return visited.get(self.end, -1)

    def is_connected_to_end(self, occupied: set[tuple[int, int]]) -> bool:
        to_visit = [(0, 0)]
        visited: set[tuple[int, int]] = set()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while len(to_visit) > 0:
            pos = to_visit.pop(0)

            for diff in directions:
                new_pos = (pos[0] + diff[0], pos[1] + diff[1])
                if new_pos not in occupied and new_pos not in visited and 0 <= new_pos[0] <= self.end[0] and 0 <= new_pos[1] <= self.end[1]:
                    to_visit.append(new_pos)
                    visited.add(new_pos)

        return self.end in visited

    def part1(self) -> int:
        occupied: set[tuple[int, int]] = {self.bytes[i] for i in range(self.part1_steps)}
        return self.find_shortest_path(occupied)

    def part2(self) -> str:
        # Do a binary search to narrow it down quickly:
        indexes_to_check = list(range(self.part1_steps, len(self.bytes)))
        while len(indexes_to_check) > 2:
            midpoint = len(indexes_to_check) // 2
            index = indexes_to_check[midpoint]
            occupied: set[tuple[int, int]] = {self.bytes[i] for i in range(index)}
            is_connected = self.is_connected_to_end(occupied)
            indexes_to_check = indexes_to_check[midpoint:] if is_connected else indexes_to_check[:midpoint + 1]

        for index in indexes_to_check:
            occupied = {self.bytes[i] for i in range(index)}
            if self.is_connected_to_end(occupied):
                byte = self.bytes[index]
                return f"{byte[0]},{byte[1]}"

        return ""

class Day18Example(Day18Base):
    def __init__(self) -> None:
        super().__init__(12, (6,6), 22, "6,1", True)

class Day18(Day18Base):
    def __init__(self) -> None:
        super().__init__(1024, (70,70), 310, "16,46", False)

if __name__ == "__main__":
    # Day18Example().check()
    Day18().check()
