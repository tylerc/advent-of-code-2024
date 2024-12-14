import copy
import re
from dataclasses import dataclass

from util import Day


@dataclass
class Robot:
    pos: tuple[int, int]
    vel: tuple[int, int]

    def tick(self, width: int, height: int) -> None:
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])

        # If they walk off the grid, wrap them around:
        if self.pos[0] < 0:
            self.pos = (width + self.pos[0], self.pos[1])
        elif self.pos[0] >= width:
            self.pos = (self.pos[0] - width, self.pos[1])

        if self.pos[1] < 0:
            self.pos = (self.pos[0], height + self.pos[1])
        elif self.pos[1] >= height:
            self.pos = (self.pos[0], self.pos[1] - height)

    def quadrant(self, width: int, height: int) -> None | int:
        midpoint_x = width // 2
        midpoint_y = height // 2

        # If you're exactly on the midpoint, you're not in any quadrant:
        if self.pos[0] == midpoint_x or self.pos[1] == midpoint_y:
            return None

        if self.pos[0] < midpoint_x and self.pos[1] < midpoint_y:
            return 1
        if self.pos[0] < midpoint_x and self.pos[1] > midpoint_y:
            return 2
        if self.pos[0] > midpoint_x and self.pos[1] < midpoint_y:
            return 3
        return 4

class Day14Base(Day):
    def __init__(
            self,
            width: int,
            height: int,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(14, part1_expect, part2_expect, example)
        self.width = width
        self.height = height
        self.starting_robots: list[Robot] = []

        for line in self.lines:
            matches = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
            assert isinstance(matches, re.Match)
            self.starting_robots.append(Robot(
                pos=(int(matches[1]), int(matches[2])),
                vel=(int(matches[3]), int(matches[4])),
            ))

    def part1(self) -> int:
        robots = copy.deepcopy(self.starting_robots)
        for _ in range(100):
            for robot in robots:
                robot.tick(self.width, self.height)

        quadrant_counts: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}
        for robot in robots:
            quadrant = robot.quadrant(self.width, self.height)
            if quadrant is not None:
                quadrant_counts[quadrant] += 1

        return quadrant_counts[1] * quadrant_counts[2] * quadrant_counts[3] * quadrant_counts[4]

    def part2(self) -> int:
        robots = copy.deepcopy(self.starting_robots)
        ticks = 0
        diffs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while True:
            ticks += 1

            occupied: set[tuple[int, int]] = set()
            for robot in robots:
                robot.tick(self.width, self.height)
                occupied.add(robot.pos)

            touching = 0
            for robot in robots:
                for diff in diffs:
                    new_pos = (robot.pos[0] + diff[0], robot.pos[1] + diff[1])
                    if new_pos in occupied:
                        touching += 1
                        break

            if touching > 300:
                break

        return ticks

class Day14Example(Day14Base):
    def __init__(self) -> None:
        super().__init__(11, 7, 12, None, True)

class Day14(Day14Base):
    def __init__(self) -> None:
        super().__init__(101, 103, 229069152, 7383, False)

if __name__ == "__main__":
    # Day14Example().check()
    Day14().check()
