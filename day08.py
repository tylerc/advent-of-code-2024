from __future__ import annotations

from util import Day


class Day08Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(8, part1_expect, part2_expect, example)
        self.antenna_types: set[str] = set()
        self.antenna_locations_by_type: dict[str, list[tuple[int, int]]] = {}
        self.width = len(self.lines[0])
        self.height = len(self.lines)
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                if char != ".":
                    self.antenna_types.add(char)
                    self.antenna_locations_by_type.setdefault(char, []).append((x, y))

    def part1(self) -> int:
        possible_antinodes: set[tuple[int, int]] = set()

        for locations in self.antenna_locations_by_type.values():
            for index, location_a in enumerate(locations):
                for location_b in locations[index + 1:]:
                    dist = (location_a[0] - location_b[0], location_a[1] - location_b[1])
                    antinode_a = (location_a[0] + dist[0], location_a[1] + dist[1])
                    antinode_b = (location_b[0] - dist[0], location_b[1] - dist[1])
                    possible_antinodes.add(antinode_a)
                    possible_antinodes.add(antinode_b)

        result = 0
        for antinode in possible_antinodes:
            if 0 <= antinode[0] < self.width and 0 <= antinode[1] < self.height:
                result += 1

        return result

    def part2(self) -> int:
        antinodes: set[tuple[int, int]] = set()

        for locations in self.antenna_locations_by_type.values():
            for index, location_a in enumerate(locations):
                antinodes.add(location_a)

                for location_b in locations[index + 1:]:
                    dist = (location_a[0] - location_b[0], location_a[1] - location_b[1])
                    antinode_a = (location_a[0] + dist[0], location_a[1] + dist[1])
                    antinode_b = (location_b[0] - dist[0], location_b[1] - dist[1])

                    while 0 <= antinode_a[0] < self.width and 0 <= antinode_a[1] < self.height:
                        antinodes.add(antinode_a)
                        antinode_a = (antinode_a[0] + dist[0], antinode_a[1] + dist[1])

                    while 0 <= antinode_b[0] < self.width and 0 <= antinode_b[1] < self.height:
                        antinodes.add(antinode_b)
                        antinode_b = (antinode_b[0] - dist[0], antinode_b[1] - dist[1])

        return len(antinodes)

class Day08Example(Day08Base):
    def __init__(self) -> None:
        super().__init__(14, 34, True)

class Day08(Day08Base):
    def __init__(self) -> None:
        super().__init__(394, 1277, False)

if __name__ == "__main__":
    # Day08Example().check()
    Day08().check()
