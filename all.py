from time import time

from day01 import Day01
from day02 import Day02
from day03 import Day03
from day04 import Day04
from day05 import Day05
from day06 import Day06
from day07 import Day07
from day08 import Day08
from day09 import Day09
from day10 import Day10
from day11 import Day11
from day12 import Day12
from day13 import Day13
from day14 import Day14
from day15 import Day15
from day16 import Day16
from day17 import Day17
from day18 import Day18
from util import columns

start = time()
days = [
    Day01(), Day02(), Day03(), Day04(), Day05(), Day06(), Day07(), Day08(), Day09(), Day10(), Day11(), Day12(), Day13(),
    Day14(), Day15(), Day16(), Day17(), Day18(),
]
print("+--------+------------+---------------------+-----------------+")
for day in days:
    day.check()
columns(None, "", "", time() - start)
print("+--------+------------+---------------------+-----------------+")
