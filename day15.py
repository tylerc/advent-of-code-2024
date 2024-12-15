from __future__ import annotations

from enum import Enum

from util import Day


class Entity(Enum):
    WALL = 0
    BOX = 1
    BOX_LEFT = 2
    BOX_RIGHT = 3
    ROBOT = 4

    @staticmethod
    def from_char(c: str) -> Entity:
        if c == "#":
            return Entity.WALL
        if c == "O":
            return Entity.BOX
        if c == "@":
            return Entity.ROBOT
        msg = f"Unknown character '{c}'"
        raise ValueError(msg)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def dir_from_char(c: str) -> tuple[int, int]:
    if c == "^":
        return UP
    if c == "v":
        return DOWN
    if c == "<":
        return LEFT
    if c == ">":
        return RIGHT
    msg = f"Unknown character '{c}'"
    raise ValueError(msg)

class Day15Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(15, part1_expect, part2_expect, example)

        self.grid_initial: dict[tuple[int, int], Entity] = {}
        self.grid_initial2: dict[tuple[int, int], Entity] = {}
        self.instructions: list[tuple[int, int]] = []

        index = self.lines.index("")
        grid_lines = self.lines[:index]
        instruction_lines = self.lines[index + 1 :]
        self.width = len(self.lines[0])
        self.height = len(grid_lines)
        self.start = (-1, -1)
        self.start2 = (-1, -1)

        for y in range(self.height):
            for x in range(self.width):
                c = grid_lines[y][x]
                if c != ".":
                    entity = Entity.from_char(c)
                    self.grid_initial[(x, y)] = entity

                    if entity == Entity.ROBOT:
                        self.grid_initial2[(x * 2, y)] = Entity.ROBOT
                        self.start = (x, y)
                        self.start2 = (x * 2, y)
                    elif entity == Entity.BOX:
                        self.grid_initial2[(x * 2, y)] = Entity.BOX_LEFT
                        self.grid_initial2[(x * 2 + 1, y)] = Entity.BOX_RIGHT
                    else:
                        self.grid_initial2[(x * 2, y)] = entity
                        self.grid_initial2[(x * 2 + 1, y)] = entity

        for line in instruction_lines:
            for char in line:
                self.instructions.append(dir_from_char(char))

    @staticmethod
    def touching(
        grid: dict[tuple[int, int], Entity],
        start: tuple[int, int],
        direction: tuple[int, int],
    ) -> tuple[set[tuple[int, int, Entity]], set[Entity]]:
        positions: set[tuple[int, int, Entity]] = set()
        entities: set[Entity] = set()
        current = start
        while current in grid:
            entity = grid[current]
            positions.add((current[0], current[1], entity))
            entities.add(entity)

            if current != start and direction in (UP, DOWN):
                if entity == Entity.BOX_LEFT:
                    other_positions, other_entities = Day15Base.touching(grid, (current[0] + 1, current[1]), direction)
                elif entity == Entity.BOX_RIGHT:
                    other_positions, other_entities = Day15Base.touching(grid, (current[0] - 1, current[1]), direction)
                else:
                    other_positions = set()
                    other_entities = set()

                for other_pos in other_positions:
                    positions.add(other_pos)
                for other_entity in other_entities:
                    entities.add(other_entity)

            current = (current[0] + direction[0], current[1] + direction[1])

        return positions, entities

    def simulate(self, grid: dict[tuple[int, int], Entity], start: tuple[int, int]) -> int:
        current = start
        for instruction in self.instructions:
            positions_to_move, entities = self.touching(grid, current, instruction)
            if Entity.WALL in entities:
                continue
            for x, y, _ in positions_to_move:
                del grid[(x, y)]
            for (x, y, entity) in positions_to_move:
                new_pos = (x + instruction[0], y + instruction[1])
                grid[new_pos] = entity
                if entity == Entity.ROBOT:
                    current = new_pos

        result = 0
        for (x, y), entity in grid.items():
            if entity in (Entity.BOX, Entity.BOX_LEFT):
                result += y * 100 + x
        return result

    def part1(self) -> int:
        return self.simulate(self.grid_initial, self.start)

    def part2(self) -> int:
        return self.simulate(self.grid_initial2, self.start2)

class Day15Example(Day15Base):
    def __init__(self) -> None:
        super().__init__(10092, 9021, True)

class Day15(Day15Base):
    def __init__(self) -> None:
        super().__init__(1294459, 1319212, False)

if __name__ == "__main__":
    # Day15Example().check()
    Day15().check()
