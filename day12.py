from collections.abc import Iterator
from dataclasses import dataclass

from util import Day


@dataclass
class Region:
    id: int
    kind: str
    points: set[tuple[int, int]]

    def extents(self):
        min_x, min_y = next(iter(self.points))
        max_x, max_y = next(iter(self.points))
        for (x, y) in self.points:
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)
        return (min_x, min_y), (max_x, max_y)

    def __hash__(self) -> int:
        return hash(self.id)

class Day12Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(12, part1_expect, part2_expect, example)

        self.grid: dict[tuple[int, int], str] = {}
        self.regions: dict[tuple[int, int], Region] = {}
        self.distinct_regions: set[Region] = set()
        self.width = len(self.lines[0])
        self.height = len(self.lines)

        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                self.grid[(x, y)] = char

        for region_id, (point, kind) in enumerate(self.grid.items()):
            region = self.regions.get(point)
            if region:
                continue
            region = Region(id=region_id, kind=kind, points={point})
            self.regions[point] = region
            self.distinct_regions.add(region)

            to_visit = set(self.adjacent(point))
            visited = {point}
            while len(to_visit) > 0:
                new_point = to_visit.pop()
                if new_point in visited:
                    continue
                visited.add(new_point)

                new_kind = self.grid.get(new_point)
                if kind == new_kind:
                    to_visit.update(self.adjacent(new_point))
                    region.points.add(new_point)
                    self.regions[new_point] = region

    @staticmethod
    def adjacent(point: tuple[int, int]) -> Iterator[tuple[int, int]]:
        diffs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for diff in diffs:
            new_point = (point[0] + diff[0], point[1] + diff[1])
            yield new_point

    def price_perimeter(self, region: Region) -> int:
        area = len(region.points)
        perimeter = 0

        for point in region.points:
            for other_point in self.adjacent(point):
                other_region = self.regions.get(other_point)
                if region != other_region:
                    perimeter += 1

        return area * perimeter

    def sides_count_horizontally(self, region: Region, x_range: range, y_range: range, diff: int) -> int:
        sides = 0

        for y in y_range:
            placing = False
            for x in x_range:
                if self.regions.get((x, y)) != region and self.regions.get((x, y + diff)) == region:
                    if not placing:
                        placing = True
                        sides += 1
                elif placing:
                    placing = False

        return sides

    def sides_count_vertically(self, region: Region, x_range: range, y_range: range, diff: int) -> int:
        sides = 0

        for x in x_range:
            placing = False
            for y in y_range:
                if self.regions.get((x, y)) != region and self.regions.get((x + diff, y)) == region:
                    if not placing:
                        placing = True
                        sides += 1
                elif placing:
                    placing = False

        return sides

    def price_sides(self, region: Region) -> int:
        area = len(region.points)
        sides = 0

        top_left, bottom_right = region.extents()
        x_range = range(top_left[0] - 1, bottom_right[0] + 2)
        y_range = range(top_left[1] - 1, bottom_right[1] + 2)

        sides += self.sides_count_horizontally(region, x_range, y_range, 1)
        sides += self.sides_count_horizontally(region, x_range, y_range, -1)
        sides += self.sides_count_vertically(region, x_range, y_range, 1)
        sides += self.sides_count_vertically(region, x_range, y_range, -1)

        return area * sides

    def part1(self) -> int:
        return sum([self.price_perimeter(region) for region in self.distinct_regions])

    def part2(self) -> int:
        return sum([self.price_sides(region) for region in self.distinct_regions])

class Day12Example(Day12Base):
    def __init__(self) -> None:
        super().__init__(1930, 1206, True)

class Day12(Day12Base):
    def __init__(self) -> None:
        super().__init__(1363682, 787680, False)

if __name__ == "__main__":
    Day12Example().check()
    Day12().check()
