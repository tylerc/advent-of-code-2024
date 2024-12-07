from abc import ABCMeta, abstractmethod
from datetime import timedelta
from pathlib import Path
from time import time


def time_diff_format(seconds: float) -> str:
    delta = timedelta(seconds=seconds)
    if delta.seconds > 0:
        return str(delta)
    if delta.microseconds > 1000:
        return f"{delta.microseconds / 1000}ms"
    return f"{delta.microseconds}μs"

def columns(day: int | None, label: str, value: str, time_diff: float) -> None:
    day_str = "All   " if day is None else f"Day {day:2}"
    print(f"| {day_str} | {label:10} | {value:10} | {time_diff_format(time_diff):15} |")

class Day(metaclass=ABCMeta):
    def __init__(
            self,
            day: int,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool = False,
    ) -> None:
        self.day = day
        self.part1_expect = part1_expect
        self.part2_expect = part2_expect

        day_str: str = str(day)
        if len(day_str) == 1:
            day_str = "0" + day_str
        filename = "day" + day_str + ".example.txt" if example else "day" + day_str + ".txt"
        self.text = (Path(__file__).parent / "inputs" / filename).read_text()
        self.lines = self.text.splitlines()
        self.setup_start = time()

    @abstractmethod
    def part1(self) -> str | int | None: pass
    @abstractmethod
    def part2(self) -> str | int | None: pass

    def check(self) -> None:
        setup_duration = time() - self.setup_start
        columns(self.day, "Setup", "", setup_duration)

        part1_start = time()
        part1_result = self.part1()
        part1_duration = time() - part1_start
        columns(self.day, "Part 1", str(part1_result), part1_duration)
        if part1_result is None:
            return
        if self.part1_expect is not None and part1_result != self.part1_expect:
            msg = f"For Part 1, expected {self.part1_expect} but got {part1_result}"
            raise ValueError(msg)

        part2_start = time()
        part2_result = self.part2()
        part2_duration = time() - part2_start
        columns(self.day, "Part 2", str(part2_result), part2_duration)
        if part2_result is None:
            return
        if self.part2_expect is not None and part2_result != self.part2_expect:
            msg = f"For Part 2, expected {self.part2_expect} but got {part2_result}"
            raise ValueError(msg)

        columns(self.day, "Total", "", setup_duration + part1_duration + part2_duration)
