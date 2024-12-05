from time import time

from day01 import Day01
from day02 import Day02
from day03 import Day03
from day04 import Day04
from util import columns

start = time()
days = [Day01, Day02, Day03, Day04]
print("+--------+------------+------------+------------+")
for day in days:
    day().check()
columns(None, "", "", time() - start)
print("+--------+------------+------------+------------+")
