from util import Day


class Day01(Day):
    def __init__(self) -> None:
        super().__init__(1, 2344935, 27647262)
        list_a: list[int] = []
        list_b: list[int] = []

        for line in self.lines:
            [a, b] = line.split("   ")
            list_a.append(int(a))
            list_b.append(int(b))

        list_a.sort()
        list_b.sort()
        self.list_a = list_a
        self.list_b = list_b

    def part1(self) -> int:
        diff: int = 0

        for x, y in zip(self.list_a, self.list_b, strict=False):
            diff += abs(x - y)

        return diff

    def part2(self) -> int:
        occurrences: dict[int, int] = {}
        similarity_score: int = 0

        for num in self.list_b:
            occurrences[num] = occurrences.get(num, 0) + 1

        for num in self.list_a:
            similarity_score += num * occurrences.get(num, 0)

        return similarity_score

if __name__ == "__main__":
    Day01().check()
