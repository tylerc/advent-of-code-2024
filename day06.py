from __future__ import annotations

from enum import Enum

from util import Day

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def rotated(point: tuple[int, int]) -> tuple[int, int]:
    if point == UP:
        return RIGHT
    if point == RIGHT:
        return DOWN
    if point == DOWN:
        return LEFT
    return UP

class Contents(Enum):
    EMPTY = 0
    OBSTRUCTION = 1
    START = 2

class Day06Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(6, part1_expect, part2_expect, example)
        self.grid: dict[tuple[int, int], Contents] = {}
        self.start: tuple[int, int] = (0, 0)
        self.width = len(self.lines[0])
        self.height = len(self.lines)

        for x in range(self.width):
            for y in range(self.height):
                pos = (x, y)
                char = self.lines[y][x]
                if char == "#":
                    self.grid[pos] = Contents.OBSTRUCTION
                elif char == "^":
                    self.grid[pos] = Contents.START
                    self.start = pos

    def grid_to_visited(self, grid: dict[tuple[int, int], Contents]) -> set[tuple[int, int]]:
        current = self.start
        direction = UP
        visited: set[tuple[int, int]] = set()

        while 0 <= current[0] < self.width and 0 <= current[1] < self.height:
            visited.add(current)
            next_point = (current[0] + direction[0], current[1] + direction[1])
            contents = grid.get(next_point)
            if contents == Contents.OBSTRUCTION:
                direction = rotated(direction)
            else:
                current = next_point

        return visited

    def grid_causes_loop(self, grid: dict[tuple[int, int], Contents]) -> bool:
        current = self.start
        direction = UP
        turns: set[tuple[tuple[int, int], tuple[int, int]]] = {(self.start, direction)}

        while 0 <= current[0] < self.width and 0 <= current[1] < self.height:
            next_point = (current[0] + direction[0], current[1] + direction[1])
            if grid.get(next_point) == Contents.OBSTRUCTION:
                direction = rotated(direction)
                current_and_direction = (current, direction)
                if current_and_direction in turns:
                    return True
                turns.add(current_and_direction)
            else:
                current = next_point

        return False

    def part1(self) -> int:
        return len(self.grid_to_visited(self.grid))

    def part2(self) -> int:
        loop_placements = 0
        points_originally_visited = self.grid_to_visited(self.grid)
        for point in points_originally_visited:
            if point == self.start:
                continue

            self.grid[point] = Contents.OBSTRUCTION
            if self.grid_causes_loop(self.grid):
                loop_placements += 1
            del self.grid[point]

        return loop_placements

class Day06Example(Day06Base):
    def __init__(self) -> None:
        super().__init__(41, 6, True)

class Day06(Day06Base):
    def __init__(self) -> None:
        super().__init__(4696, 1443, False)

if __name__ == "__main__":
    # Day06Example().check()
    Day06().check()
