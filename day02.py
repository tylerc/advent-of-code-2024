import itertools

from util import Day


class Day02(Day):
    def __init__(self) -> None:
        super().__init__(2, 686, 717)
        self.reports: list[list[int]] = []
        for line in self.lines:
            split = line.split(" ")
            self.reports.append([int(chars) for chars in split])

    @staticmethod
    def is_safe(report: list[int]) -> bool:
        increasing = False
        decreasing = False
        wrong_difference = False

        for a, b in itertools.pairwise(report):
            diff = abs(a - b)
            if diff < 1 or diff > 3:
                wrong_difference = True
                break

            if a > b:
                increasing = True
            elif a < b:
                decreasing = True

        return (increasing ^ decreasing) and not wrong_difference

    def part1(self) -> int:
        safe_count = 0
        for report in self.reports:
            if self.is_safe(report):
                safe_count += 1

        return safe_count

    def part2(self) -> int:
        safe_count = 0
        for report in self.reports:
            if self.is_safe(report):
                safe_count += 1
            else:
                for i in range(len(report)):
                    new_report: list[int] = []
                    for j, num in enumerate(report):
                        if i != j:
                            new_report.append(num)

                    if self.is_safe(new_report):
                        safe_count += 1
                        break

        return safe_count

if __name__ == "__main__":
    Day02().check()
