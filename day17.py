from __future__ import annotations

import copy
from collections.abc import Iterator
from dataclasses import dataclass, field

from util import Day


@dataclass
class Computer:
    registers: dict[str, int]
    program: list[int]
    instruction_pointer: int = 0
    output_str: str = ""
    output_list: list[int] = field(default_factory=list)
    is_halted: bool = False

    def combo_operand(self, val: int) -> int:
        if val in (0, 1, 2, 3):
            return val
        if val == 4:
            return self.registers["A"]
        if val == 5:
            return self.registers["B"]
        if val == 6:
            return self.registers["C"]
        msg = f"invalid combo operand: {val}"
        raise ValueError(msg)

    def process_instruction(self) -> None:
        opcode = self.program[self.instruction_pointer] if self.instruction_pointer < len(self.program) else None
        operand = self.program[self.instruction_pointer + 1] if self.instruction_pointer + 1 < len(self.program) else None
        self.instruction_pointer += 2

        if opcode is None or operand is None:
            self.is_halted = True
            return

        if opcode == 0: # adv
            operand = self.combo_operand(operand)
            self.registers["A"] = self.registers["A"] // (2 ** operand)
        elif opcode == 1: # bxl
            self.registers["B"] = self.registers["B"] ^ operand
        elif opcode == 2: # bst
            operand = self.combo_operand(operand)
            self.registers["B"] = operand % 8
        elif opcode == 3: # jnz
            if self.registers["A"] != 0:
                self.instruction_pointer = operand
        elif opcode == 4: # bxc
            self.registers["B"] = self.registers["B"] ^ self.registers["C"]
        elif opcode == 5: # output
            operand = self.combo_operand(operand)
            output = operand % 8
            if self.output_str:
                self.output_str += ","
            self.output_str += str(output)
            self.output_list.append(output)
        elif opcode == 6: # bdv
            operand = self.combo_operand(operand)
            self.registers["B"] = self.registers["A"] // (2 ** operand)
        elif opcode == 7: # cdv
            operand = self.combo_operand(operand)
            self.registers["C"] = self.registers["A"] // (2 ** operand)

    def run_to_end(self) -> str:
        while not self.is_halted:
            self.process_instruction()
        return self.output_str

class Day17Base(Day):
    def __init__(
            self,
            part1_expect: str | int | None,
            part2_expect: str | int | None,
            example: bool,
    ) -> None:
        super().__init__(17, part1_expect, part2_expect, example)
        self.computer = Computer(
            registers={
                "A": int(self.lines[0].split(": ")[1]),
                "B": int(self.lines[1].split(": ")[1]),
                "C": int(self.lines[2].split(": ")[1]),
            },
            program=[int(s) for s in self.lines[4].split(": ")[1].split(",")],
        )

        # If register C contains 9, the program 2,6 would set register B to 1.
        # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
        # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
        # If register B contains 29, the program 1,7 would set register B to 26.
        # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
        test_1 = Computer(registers={"A": 0, "B": 0, "C": 9}, program=[2,6])
        test_1.run_to_end()
        assert test_1.registers["B"] == 1

        test_2 = Computer(registers={"A": 10, "B": 0, "C": 0}, program=[5,0,5,1,5,4])
        assert test_2.run_to_end() == "0,1,2"

        test_3 = Computer(registers={"A": 2024, "B": 0, "C": 0}, program=[0,1,5,4,3,0])
        assert test_3.run_to_end() == "4,2,5,6,7,7,7,7,3,1,0"
        assert test_3.registers["A"] == 0

        test_4 = Computer(registers={"A": 0, "B": 29, "C": 0}, program=[1,7])
        test_4.run_to_end()
        assert test_4.registers["B"] == 26

        test_5 = Computer(registers={"A": 0, "B": 2024, "C": 43690}, program=[4,0])
        test_5.run_to_end()
        assert test_5.registers["B"] == 44354

    @staticmethod
    def list_to_num(inputs: list[int]) -> int:
        """Given a list of 3-bit integers, combine them together to build a single integer."""
        num = 0
        for index in range(len(inputs)):
            num |= inputs[index] << ((len(inputs) - index - 1) * 3)
        return num

    def find_matches(self, inputs: list[int], wanted: list[int], input_index_changing: int) -> Iterator[list[int]]:
        for i in range(8):
            inputs_copy = inputs[:]
            inputs_copy[input_index_changing] = i
            num = self.list_to_num(inputs_copy)
            computer = copy.deepcopy(self.computer)
            computer.registers["A"] = num
            computer.run_to_end()
            if computer.output_list[-input_index_changing - 1] == wanted[-input_index_changing - 1]:
                yield inputs_copy

    def part1(self) -> str:
        return copy.deepcopy(self.computer).run_to_end()

    # Upon closer examination of my input, I noticed several things:
    # 1. We have a single, simple loop wrapping the whole program that exits when A is 0.
    # 2. B and C are used as scratch registers, and no state is persisted in them between loop iterations.
    # 3. The 3 least significant bits are used from A when computing the output (along with some other bits too).
    # 4. A is divided by 8 after each loop, which is equivalent to shifting the 3 least significant bits off.
    #
    # From those observations, it seemed reasonable that I could fiddle with 3 bits of input at a time, and find
    # a value that yields the correct result for the next 3 bits of output. This worked!
    #
    # Some caveats:
    # 1. For some bits, multiple patterns result in the correct output. So need to keep track of several possibilities.
    # 2. There is more than one input that yields the correct output, so we have to collect them all and then select
    #    the smallest.
    def part2(self) -> int:
        to_try = [([0b111 for _ in range(len(self.computer.program))], 0)]
        results: list[list[int]] = []

        while len(to_try) > 0:
            inputs, index = to_try.pop()
            for candidate in self.find_matches(inputs, self.computer.program, index):
                if index == len(self.computer.program) - 1:
                    results.append(candidate)
                else:
                    to_try.append((candidate, index + 1))

        return min(self.list_to_num(result) for result in results)

class Day17Example(Day17Base):
    def __init__(self) -> None:
        super().__init__("4,6,3,5,6,3,5,2,1,0", None, True)

class Day17(Day17Base):
    def __init__(self) -> None:
        super().__init__("6,5,7,4,5,7,3,1,0", 105875099912602, False)

if __name__ == "__main__":
    # Day17Example().check()
    Day17().check()
