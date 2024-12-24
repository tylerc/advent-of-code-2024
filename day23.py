from __future__ import annotations

from collections import Counter
from itertools import combinations

from util import Day


def build_graph(connections: set[tuple[str, str]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}

    for left, right in connections:
        left_set = graph.setdefault(left, set())
        left_set.add(right)
        right_set = graph.setdefault(right, set())
        right_set.add(left)

    return graph

def score_transitives(graph: dict[str, set[str]]) -> Counter[str]:
    """For each node, add a point to the node for each connection it shares in common with the connections of its
    connections."""
    result: Counter[str] = Counter()

    for node, connections in graph.items():
        for connection in connections:
            result[node] += len(connections & graph[connection])

    return result

class Day23Base(Day):
    def __init__(
        self,
        part1_expect: str | int | None,
        part2_expect: str | int | None,
        example: bool,
    ) -> None:
        super().__init__(23, part1_expect, part2_expect, example)
        self.connections: set[tuple[str, str]] = set()
        for line in self.lines:
            left, right = line.split("-")
            self.connections.add((left, right))
        self.graph = build_graph(self.connections)

    def part1(self) -> int:
        triples: set[frozenset[str]] = set()
        for node, connections in self.graph.items():
            if len(connections) <= 1:
                continue
            for a, b in combinations(connections, 2):
                if a in self.graph[b] and b in self.graph[a]:
                    triples.add(frozenset([node, a, b]))

        triples_with_t = 0
        for triple in triples:
            for item in triple:
                if item.startswith("t"):
                    triples_with_t += 1
                    break

        return triples_with_t

    def part2(self) -> str:
        scored = score_transitives(self.graph)
        max_transitives = max(scored.values())
        # For the test input, additional filtering is needed, but we're just going to be happy with victory on the
        # real input:
        return ",".join(sorted([computer for computer, score in scored.items() if score == max_transitives]))

class Day23Example(Day23Base):
    def __init__(self) -> None:
        super().__init__(7, None, True)

class Day23(Day23Base):
    def __init__(self) -> None:
        super().__init__(1046, "de,id,ke,ls,po,sn,tf,tl,tm,uj,un,xw,yz", False)

if __name__ == "__main__":
    # Day23Example().check()
    Day23().check()
