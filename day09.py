from dataclasses import dataclass
from enum import Enum

from util import Day


class BlockType(Enum):
    FILE = 0
    FREE_SPACE = 1

@dataclass
class FileId:
    id: int

@dataclass
class Item:
    id: FileId
    type: BlockType
    length: int

    def __str__(self) -> str:
        if self.type == BlockType.FILE:
            return f"FILE({self.id.id} len={self.length})"
        return f"SPACE(len={self.length})"

free_space_id = FileId(-1)

class Day09Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(9, part1_expect, part2_expect, example)
        self.blocks: list[Item] = []
        is_free_space = False
        id_next = 0
        for char in self.lines[0]:
            if is_free_space:
                self.blocks.append(Item(id=free_space_id, type=BlockType.FREE_SPACE, length=int(char)))
            else:
                self.blocks.append(Item(id=FileId(id_next), type=BlockType.FILE, length=int(char)))
                id_next += 1
            is_free_space = not is_free_space

    def part1(self) -> int:
        blocks_expanded: list[Item] = []
        for block in self.blocks:
            blocks_expanded.extend([Item(id=block.id, type=block.type, length=1) for _ in range(block.length)])

        for index in range(len(blocks_expanded)):
            while blocks_expanded[-1].type == BlockType.FREE_SPACE:
                blocks_expanded.pop()

            if index >= len(blocks_expanded):
                break

            item = blocks_expanded[index]
            if item.type == BlockType.FREE_SPACE:
                blocks_expanded[index] = blocks_expanded.pop()

        result = 0
        for index, item in enumerate(blocks_expanded):
            if item.type == BlockType.FILE:
                result += index * item.id.id
        return result

    def part2(self) -> int:
        current_id = max([item.id.id for item in self.blocks])
        while current_id >= 0:
            (file_index, file) = next((index, item) for index, item in enumerate(self.blocks) if item.id.id == current_id)
            for iter_index in range(file_index):
                item = self.blocks[iter_index]
                if item.type == BlockType.FREE_SPACE and item.length >= file.length:
                    self.blocks[iter_index] = file
                    self.blocks[file_index] = Item(id=free_space_id, type=BlockType.FREE_SPACE, length=file.length)
                    if item.length > file.length:
                        item.length -= file.length
                        self.blocks.insert(iter_index + 1, item)
                    break

            current_id -= 1

        blocks_expanded: list[Item] = []
        for block in self.blocks:
            blocks_expanded.extend([Item(id=block.id, type=block.type, length=1) for _ in range(block.length)])

        result = 0
        for index, item in enumerate(blocks_expanded):
            if item.type == BlockType.FILE:
                result += index * item.id.id
        return result

class Day09Example(Day09Base):
    def __init__(self) -> None:
        super().__init__(1928, 2858, True)

class Day09(Day09Base):
    def __init__(self) -> None:
        super().__init__(6211348208140, 6239783302560, False)

if __name__ == "__main__":
    # Day09Example().check()
    Day09().check()
