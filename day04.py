from util import Day


class Day04(Day):
    def __init__(self) -> None:
        super().__init__(4, 2557, 1854)
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def get_char(self, x: int, y: int) -> str:
        if x >= self.width or x < 0:
            return ""
        if y >= self.height or y < 0:
            return ""
        return self.lines[y][x]

    def matches_path(self, start_x: int, start_y: int, path: list[tuple[int, int]], want: tuple[str, ...]) -> bool:
        found = self.get_char(start_x, start_y)
        for item in path:
            found += self.get_char(start_x + item[0], start_y + item[1])
        return found in want

    def part1(self) -> int:
        total = 0

        right = [(1, 0), (2, 0), (3, 0)]
        down = [(0, 1), (0, 2), (0, 3)]
        south_east = [(1, 1), (2, 2), (3, 3)]
        south_west = [(-1, 1), (-2, 2), (-3, 3)]
        all_paths = [right, down, south_east, south_west]
        want = ("XMAS", "SAMX")

        for x in range(self.width):
            for y in range(self.height):
                for path in all_paths:
                    if self.matches_path(x, y, path, want):
                        total += 1

        return total

    def part2(self) -> int:
        total = 0

        x_shape = [
            # South-east:
            # (0, 0), This is implied
            (1, 1),
            (2, 2),
            # South-west:
            (2, 0),
            (1, 1),
            (0, 2),
        ]
        want = ("MASMAS", "SAMSAM", "MASSAM", "SAMMAS")

        for x in range(self.width):
            for y in range(self.height):
                if self.matches_path(x, y, x_shape, want):
                    total += 1

        return total

if __name__ == "__main__":
    Day04().check()
