from __future__ import annotations

from enum import Enum

from util import Day


class Entity(Enum):
    WALL = 0
    START = 1
    END = 2

    @staticmethod
    def from_char(c: str) -> Entity:
        if c == "#":
            return Entity.WALL
        if c == "S":
            return Entity.START
        if c == "E":
            return Entity.END
        msg = f"Unknown character '{c}'"
        raise ValueError(msg)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def turns(direction: tuple[int, int]) -> list[tuple[int, int]]:
    if direction in (UP, DOWN):
        return [LEFT, RIGHT]
    return [UP, DOWN]

class Day16Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(16, part1_expect, part2_expect, example)
        self.grid: dict[tuple[int, int], Entity] = {}
        self.width = len(self.lines[0])
        self.height = len(self.lines)
        self.start = (-1, -1)
        self.end = (-1, -1)

        for y in range(self.height):
            for x in range(self.width):
                char = self.lines[y][x]
                if char != ".":
                    entity = Entity.from_char(char)
                    self.grid[(x, y)] = entity
                    if entity == Entity.START:
                        self.start = (x, y)
                    elif entity == Entity.END:
                        self.end = (x, y)

        self.costs = self.compute_costs()

    def compute_costs(self) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
        to_visit = {(self.start, RIGHT, 0)}
        visited: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}

        while len(to_visit) > 0:
            pos, facing, cost = to_visit.pop()
            existing_cost = visited.get((pos, facing))
            if existing_cost and existing_cost < cost:
                continue
            visited[(pos, facing)] = cost

            next_pos = (pos[0] + facing[0], pos[1] + facing[1])
            if self.grid.get(next_pos) != Entity.WALL:
                to_visit.add((next_pos, facing, cost + 1))

            for turn in turns(facing):
                to_visit.add((pos, turn, cost + 1000))

        return visited

    def part1(self) -> int:
        return min(self.costs[(self.end, direction)] for direction in (UP, DOWN, LEFT, RIGHT))

    def part2(self) -> int:
        to_visit: list[tuple[tuple[int, int], tuple[int, int], int, frozenset[tuple[int, int]]]] = [
            (self.start, RIGHT, 0, frozenset([self.start])),
        ]
        visited: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
        end_paths: list[tuple[int, frozenset[tuple[int, int]]]] = []

        end_cost = self.part1()
        while len(to_visit) > 0:
            pos, facing, cost, path = to_visit.pop()
            known_lowest_cost = self.costs[(pos, facing)]
            if cost > known_lowest_cost:
                continue

            existing_cost = visited.get((pos, facing))
            if existing_cost and existing_cost < cost:
                continue

            visited[(pos, facing)] = cost

            if self.end == pos:
                if cost == end_cost:
                    end_paths.append((cost, path))
                continue

            next_pos = (pos[0] + facing[0], pos[1] + facing[1])
            if self.grid.get(next_pos) != Entity.WALL:
                to_visit.append((next_pos, facing, cost + 1, path | frozenset([next_pos])))

            for turn in turns(facing):
                to_visit.append((pos, turn, cost + 1000, path))

        tiles_in_end_paths: set[tuple[int, int]] = set()
        for (cost, path) in end_paths:
            if cost == end_cost:
                tiles_in_end_paths.update(path)

        return len(tiles_in_end_paths)

class Day16Example(Day16Base):
    def __init__(self) -> None:
        super().__init__(11048, 64, True)

class Day16(Day16Base):
    def __init__(self) -> None:
        super().__init__(73432, 496, False)

if __name__ == "__main__":
    # Day16Example().check()
    Day16().check()
