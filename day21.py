from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from util import Day

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
ACTION = (0, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def reverse(direction: tuple[int, int]) -> tuple[int, int]:
    if direction == UP:
        return DOWN
    if direction == DOWN:
        return UP
    if direction == LEFT:
        return RIGHT
    if direction == RIGHT:
        return LEFT
    msg = f"{direction} is not a direction"
    raise ValueError(msg)

def direction_to_char(direction: tuple[int, int]) -> str:
    if direction == UP:
        return "^"
    if direction == DOWN:
        return "v"
    if direction == LEFT:
        return "<"
    if direction == RIGHT:
        return ">"
    if direction == ACTION:
        return "A"
    msg = f"{direction} is not a direction"
    raise ValueError(msg)

def char_to_direction(direction: str) -> tuple[int, int]:
    if direction == "^":
        return UP
    if direction == "v":
        return DOWN
    if direction == "<":
        return LEFT
    if direction == ">":
        return RIGHT
    if direction == "A":
        return ACTION
    msg = f"{direction} is not a direction"
    raise ValueError(msg)

def directions_to_str(directions: list[tuple[int, int]]) -> str:
    return "".join(direction_to_char(direction) for direction in directions)

@dataclass
class RobotKeypad:
    keys: dict[tuple[int, int], str]
    robot_start: tuple[int, int]
    keys_reversed: dict[str, tuple[int, int]] = field(default_factory=dict)
    shortest_paths_cache: dict[tuple[tuple[int, int], tuple[int, int]], list[list[tuple[int, int]]]] = field(default_factory=dict)
    enter_cache: dict[str, list[list[tuple[int, int]]]] = field(default_factory=dict)

    def adjacent(self, pos: tuple[int, int]) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
        for direction in DIRECTIONS:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if new_pos in self.keys:
                yield direction, new_pos

    def visit_costs(self, start: tuple[int, int]) -> dict[tuple[int, int], int]:
        to_visit = {(start, 0)}
        visited: dict[tuple[int, int], int] = {}

        while len(to_visit) > 0:
            pos, cost = to_visit.pop()
            existing_cost = visited.get(pos)
            if existing_cost is not None and existing_cost <= cost:
                continue
            visited[pos] = cost

            for _, new_pos in self.adjacent(pos):
                to_visit.add((new_pos, cost + 1))

        return visited

    def shortest_paths(self, start: tuple[int, int], end: tuple[int, int]) -> list[list[tuple[int, int]]]:
        cached = self.shortest_paths_cache.get((start, end))
        if cached is not None:
            return cached

        costs = self.visit_costs(start)
        to_check: list[tuple[tuple[int, int], list[tuple[int, int]]]] = [(end, [])]
        paths: list[list[tuple[int, int]]] = []

        while len(to_check) > 0:
            current, path = to_check.pop()
            if current == start:
                paths.append(path)
                continue

            connections = [(costs[pos], direction, pos) for direction, pos in self.adjacent(current)]
            min_cost = min(cost for cost, _, _ in connections)
            for cost, direction, pos in connections:
                if cost == min_cost:
                    new_path = [reverse(direction), *path]
                    to_check.append((pos, new_path))

        shortest_path = min(len(path) for path in paths)
        result = [path for path in paths if len(path) == shortest_path]
        self.shortest_paths_cache[(start, end)] = result
        return result

    def pos_for_key(self, key: str) -> tuple[int, int]:
        cached = self.keys_reversed.get(key)
        if cached is not None:
            return cached

        for pos, other_key in self.keys.items():
            if key == other_key:
                self.keys_reversed[key] = pos
                return pos
        msg = f"{key} is not a valid for this keypad"
        raise ValueError(msg)

    def movements_required_to_enter(self, keys: str) -> list[list[tuple[int, int]]]:
        """Given a lists of keys to enter, returns lists of movements that the robot could follow to enter those keys.
        We return multiple lists because some movements may be faster for operating robots to execute even if they
        are ultimately equivalent for this robot."""
        cached = self.enter_cache.get(keys)
        if cached is not None:
            return cached

        current = self.robot_start
        paths: list[list[tuple[int, int]]] = []
        for key in keys:
            destination = self.pos_for_key(key)
            options = self.shortest_paths(current, destination)

            if len(paths) == 0:
                paths = [[*option, ACTION] for option in options]
            else:
                new_paths: list[list[tuple[int, int]]] = []
                for path in paths:
                    new_paths.extend([*path, *option, ACTION] for option in options)
                paths = new_paths

            current = destination

        shortest_path = min(len(path) for path in paths)
        result = [path for path in paths if len(path) == shortest_path]
        self.enter_cache[keys] = result
        return result

def split_on_a(splitting: str) -> Iterator[str]:
    """Splits input keys into sequences on the 'A' character, but includes the 'A'.
    So, '<AvA' becomes ['<A', 'vA']. 'A' becomes ['A']."""
    next_output = ""
    for char in splitting:
        next_output += char
        if char == "A":
            yield next_output
            next_output = ""

shortest_sequence_cache: dict[tuple[str, int], int] = {}
# This function recursively finds the shortest sequence length required for a given set of keys to be inputted into
# a keypad.
#
# A depth of 0 means no robots are involved, a human is pressing keys, and so the sequence length is the length of the
# keys to press.
#
# A depth of 1 or more means robots are involved, and so we must determine how many moves the robot takes to enter
# the required keys. We assume the first robot is operating a numpad, and all others operate dirpads. Each robot
# can tell us possible sequences of inputs it can use to enter a given sequence on its keypad.
#
# Because there is a chain of robots all operating each other, once we have a sequence of inputs that will cause a
# a robot to enter the correct keys, we must recursively figure out how to make the next robot produce that new sequence
# (our new set of keys) until we get to depth 0 (the human).
#
# The key observation that makes this work recursively is that every time a robot presses "A", it has returned to its
# starting position. So, we can chunk its keys on "A", computing the total for each small chunk. This is much faster
# than operating on the full input, and it lets us easily cache the totals at each depth level.
#
# A debt is owed to https://www.reddit.com/r/adventofcode/comments/1hjx0x4/2024_day_21_quick_tutorial_to_solve_part_2_in/
# which showed me this method. While I had many of the necessary insights and code implemented, I could not for the
# life of me figure out how to put it all together in a way that was efficient enough for part 2.
def shortest_sequence(numpad: RobotKeypad, dirpad: RobotKeypad, keys: str, depth: int, is_start: bool) -> int:
    if depth == 0:
        return len(keys)

    cached = shortest_sequence_cache.get((keys, depth))
    if cached is not None:
        return cached

    keypad = numpad if is_start else dirpad

    total = 0
    for sub_key in split_on_a(keys):
        possibilities = keypad.movements_required_to_enter(sub_key)
        minimum = min(shortest_sequence(numpad, dirpad, directions_to_str(possibility), depth - 1, False) for possibility in possibilities)
        total += minimum

    shortest_sequence_cache[(keys, depth)] = total
    return total

@dataclass
class Simulator:
    numpad: RobotKeypad
    dirpad: RobotKeypad
    numpad_robot_pos: tuple[int, int]
    dirpad_robot_1_pos: tuple[int, int]
    dirpad_robot_2_pos: tuple[int, int]
    output: str = ""

    def simulate(self, keys: str) -> str:
        for key in keys:
            if key == "A":
                key_from_2 = self.dirpad.keys[self.dirpad_robot_2_pos]
                if key_from_2 == "A":
                    key_from_1 = self.dirpad.keys[self.dirpad_robot_1_pos]
                    if key_from_1 == "A":
                        self.output += self.numpad.keys[self.numpad_robot_pos]
                    else:
                        direction = char_to_direction(key_from_1)
                        self.numpad_robot_pos = (self.numpad_robot_pos[0] + direction[0], self.numpad_robot_pos[1] + direction[1])
                else:
                    direction = char_to_direction(key_from_2)
                    self.dirpad_robot_1_pos = (self.dirpad_robot_1_pos[0] + direction[0], self.dirpad_robot_1_pos[1] + direction[1])
            else:
                direction = char_to_direction(key)
                self.dirpad_robot_2_pos = (self.dirpad_robot_2_pos[0] + direction[0], self.dirpad_robot_2_pos[1] + direction[1])

            if self.numpad.keys.get(self.numpad_robot_pos) is None:
                msg = f"Numpad robot is in invalid position: {self.numpad_robot_pos}"
                raise ValueError(msg)
            if self.dirpad.keys.get(self.dirpad_robot_1_pos) is None:
                msg = f"Dirpad robot 1 is in invalid position: {self.dirpad_robot_1_pos}"
                raise ValueError(msg)
            if self.dirpad.keys.get(self.dirpad_robot_2_pos) is None:
                msg = f"Dirpad robot 2 is in invalid position: {self.dirpad_robot_2_pos}"
                raise ValueError(msg)

        return self.output

class Day21Base(Day):
    def __init__(
        self,
        part1_expect: str | int | None,
        part2_expect: str | int | None,
        example: bool,
    ) -> None:
        super().__init__(21, part1_expect, part2_expect, example)
        self.numpad = RobotKeypad(keys={
            (0, 0): "7",
            (1, 0): "8",
            (2, 0): "9",
            (0, 1): "4",
            (1, 1): "5",
            (2, 1): "6",
            (0, 2): "1",
            (1, 2): "2",
            (2, 2): "3",
            (1, 3): "0",
            (2, 3): "A",
        }, robot_start=(2, 3))
        self.dirpad = RobotKeypad(keys={
            (1, 0): "^",
            (2, 0): "A",
            (0, 1): "<",
            (1, 1): "v",
            (2, 1): ">",
        }, robot_start=(2, 0))

        self.sim = Simulator(numpad=self.numpad, dirpad=self.dirpad, numpad_robot_pos=self.numpad.robot_start, dirpad_robot_1_pos=self.dirpad.robot_start, dirpad_robot_2_pos=self.dirpad.robot_start)

    def part1(self) -> int:
        result = 0
        for line in self.lines:
            result += shortest_sequence(self.numpad, self.dirpad, line, 1 + 2, True) * int(line[:-1])
        return result

    def part2(self) -> int:
        result = 0
        for line in self.lines:
            result += shortest_sequence(self.numpad, self.dirpad, line, 1 + 25, True) * int(line[:-1])
        return result

class Day21Example(Day21Base):
    def __init__(self) -> None:
        super().__init__(126384, None, True)

class Day21(Day21Base):
    def __init__(self) -> None:
        super().__init__(152942, 189235298434780, False)

if __name__ == "__main__":
    # Day21Example().check()
    Day21().check()
