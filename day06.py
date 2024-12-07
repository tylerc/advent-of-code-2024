from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from util import Day


class Point(NamedTuple):
    x: int
    y: int

    def add_point(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

class Dir(Enum):
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)

    def rotated(self) -> Dir:
        match self:
            case Dir.UP:
                return Dir.RIGHT
            case Dir.RIGHT:
                return Dir.DOWN
            case Dir.DOWN:
                return Dir.LEFT
            case Dir.LEFT:
                return Dir.UP

class Contents(Enum):
    EMPTY = 0
    OBSTRUCTION = 1
    START = 2

class EndCondition(Enum):
    OFF_GRID = 0
    LOOP = 1

class Day06Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(6, part1_expect, part2_expect, example)
        self.grid: dict[Point, Contents] = {}
        self.start = Point(0, 0)
        self.width = len(self.lines[0])
        self.height = len(self.lines)

        for x in range(self.width):
            for y in range(self.height):
                pos = Point(x, y)
                char = self.lines[y][x]
                if char == "#":
                    self.grid[pos] = Contents.OBSTRUCTION
                elif char == "^":
                    self.grid[pos] = Contents.START
                    self.start = pos
                else:
                    self.grid[pos] = Contents.EMPTY

    def grid_to_visited(self, grid: dict[Point, Contents]) -> tuple[set[Point], EndCondition]:
        current = self.start
        direction = Dir.UP
        visited: set[Point] = set()
        visited2: set[tuple[Point, Dir]] = set()
        end_condition = EndCondition.OFF_GRID

        while current in grid:
            visited.add(current)
            current_and_direction = (current, direction)
            if current_and_direction in visited2:
                end_condition = EndCondition.LOOP
                break
            visited2.add(current_and_direction)
            next_point = current.add_point(direction.value)
            if next_point.x >= 0 and next_point.x < self.width and next_point.y >= 0 and next_point.y < self.height:
                contents = grid[next_point]
                if contents == Contents.OBSTRUCTION:
                    direction = direction.rotated()
                else:
                    current = next_point
            else:
                break

        return visited, end_condition

    def part1(self) -> int:
        return len(self.grid_to_visited(self.grid)[0])

    def part2(self) -> int:
        loop_placements = 0
        points_originally_visited = self.grid_to_visited(self.grid)[0]
        for point in points_originally_visited:
            if point == self.start:
                continue

            new_grid = {**self.grid, point: Contents.OBSTRUCTION}
            if self.grid_to_visited(new_grid)[1] == EndCondition.LOOP:
                loop_placements += 1

        return loop_placements

class Day06Example(Day06Base):
    def __init__(self) -> None:
        super().__init__(41, 6, True)

class Day06(Day06Base):
    def __init__(self) -> None:
        super().__init__(4696, 1443, False)

if __name__ == "__main__":
    Day06Example().check()
    Day06().check()
