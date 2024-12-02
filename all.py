from time import time

from day01 import Day01
from day02 import Day02
from util import columns

start = time()
days = [Day01, Day02]
print("+--------+------------+------------+------------+")
for day in days:
    day().check()
columns(None, "", "", time() - start)
print("+--------+------------+------------+------------+")
