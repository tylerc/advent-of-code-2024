from __future__ import annotations

from dataclasses import dataclass
from random import randint

from util import Day


@dataclass(frozen=True)
class Gate:
    left: str
    right: str
    operator: str
    output: str

    def match_inputs_and_operator(self, other: Gate) -> bool:
        inputs = (self.left, self.right)
        return other.left in inputs and other.right in inputs and self.operator == other.operator

    def match_output_operator_and_single_input(self, other: Gate) -> bool:
        inputs = (self.left, self.right)
        return (other.left in inputs or other.right in inputs) and self.operator == other.operator and self.output == other.output

    def evaluate(self, evaluated: dict[str, int]) -> int:
        left = evaluated[self.left]
        right = evaluated[self.right]

        if self.operator == "AND":
            return left & right
        if self.operator == "OR":
            return left | right
        if self.operator == "XOR":
            return left ^ right
        msg = f"Unexpected operator: {self.operator}"
        raise ValueError(msg)

class Day24Base(Day):
    def __init__(
        self,
        part1_expect: str | int | None,
        part2_expect: str | int | None,
        example: bool,
    ) -> None:
        super().__init__(24, part1_expect, part2_expect, example)
        midpoint = self.lines.index("")
        self.starting_values: dict[str, int] = {}

        for line in self.lines[:midpoint]:
            label, value = line.split(": ")
            self.starting_values[label] = int(value)

        self.gates: set[Gate] = set()
        self.gates_by_output: dict[str, Gate] = {}
        for line in self.lines[midpoint+1:]:
            left, operator, right, _, output = line.split(" ")
            gate = Gate(left=left, right=right, operator=operator, output=output)
            self.gates.add(gate)
            self.gates_by_output[output] = gate

    @staticmethod
    def evaluate(starting_values: dict[str, int], gates: set[Gate]) -> int:
        evaluated = starting_values.copy()
        to_evaluate = gates.copy()

        while len(to_evaluate) > 0:
            to_remove: set[Gate] = set()
            for item in to_evaluate:
                if item.left in evaluated and item.right in evaluated:
                    evaluated[item.output] = item.evaluate(evaluated)
                    to_remove.add(item)
            for item in to_remove:
                to_evaluate.remove(item)
            if len(to_remove) == 0:
                msg = f"Failed to remove from {to_evaluate}"
                raise ValueError(msg)

        z_vars = sorted([key for key in evaluated if key.startswith("z")])
        number_building = 0
        for var in z_vars:
            shift = int(var[1:])
            number_building |= evaluated[var] << shift

        return number_building

    @staticmethod
    def build_adder_gates(max_id: int, comparison_gates: set[Gate]) -> set[Gate]:
        gates: set[Gate] = set()
        to_find = comparison_gates.copy()

        # TODO: 1. Ideally we'd find these automatically, but we found them manually instead:
        to_find.remove(Gate(left="x09", right="y09", operator="AND", output="kfp"))
        to_find.remove(Gate(left="y09", right="x09", operator="XOR", output="hbs"))
        to_find.add(Gate(left="x09", right="y09", operator="AND", output="hbs"))
        to_find.add(Gate(left="y09", right="x09", operator="XOR", output="kfp"))

        to_find.remove(Gate(left="x18", right="y18", operator="AND", output="z18"))
        to_find.remove(Gate(left="pvk", right="fwt", operator="XOR", output="dhq"))
        to_find.add(Gate(left="x18", right="y18", operator="AND", output="dhq"))
        to_find.add(Gate(left="pvk", right="fwt", operator="XOR", output="z18"))

        to_find.remove(Gate(left="dcm", right="dbp", operator="XOR", output="pdg"))
        to_find.remove(Gate(left="bqp", right="gkg", operator="OR", output="z22"))
        to_find.add(Gate(left="dcm", right="dbp", operator="XOR", output="z22"))
        to_find.add(Gate(left="bqp", right="gkg", operator="OR", output="pdg"))

        to_find.remove(Gate(left="ckj", right="bch", operator="XOR", output="jcp"))
        to_find.remove(Gate(left="ckj", right="bch", operator="AND", output="z27"))
        to_find.add(Gate(left="ckj", right="bch", operator="XOR", output="z27"))
        to_find.add(Gate(left="ckj", right="bch", operator="AND", output="jcp"))

        name_mapping: dict[str, str] = {}

        def add_and_check(gate: Gate) -> None:
            if gate.left.startswith("x"):
                matching_gate = next((other_gate for other_gate in to_find if other_gate.match_inputs_and_operator(gate)), None)
                if matching_gate is None:
                    msg = f"Unable to find input gate: {gate}"
                    raise ValueError(msg)
                name_mapping[matching_gate.output] = gate.output
                name_mapping[gate.output] = matching_gate.output
            else:
                rewritten = Gate(left=name_mapping.get(gate.left, gate.left), right=name_mapping.get(gate.right, gate.right), operator=gate.operator, output=name_mapping.get(gate.output, gate.output))
                matching_gate = next((other_gate for other_gate in to_find if other_gate.match_inputs_and_operator(rewritten)), None)
                # Presumably one of our prior associations is wrong!
                if matching_gate is None:
                    print(f"Failed to find {gate} {rewritten}")
                    # print([other_gate for other_gate in to_find if other_gate.output in (rewritten.left, rewritten.right)])
                    # print([other_gate for other_gate in to_find if other_gate.operator == rewritten.operator and len({other_gate.left, other_gate.right} & {rewritten.left, rewritten.right}) > 0])
                    # While this was helpful for the first two, it wasn't so helpful for the latter two:
                    # bad1 = next(other_gate for other_gate in to_find if
                    #        other_gate.output in (rewritten.left, rewritten.right) and (other_gate.left.startswith("x") or other_gate.right.startswith("x")))
                    # print(bad1)

                    # This seems to be reliable at identifying _one_ of them:
                    # Find a gate that nearly matches, which is likely the gate we should've found but couldn't due to
                    # the bad name mapping:
                    almost_matches = next((other_gate for other_gate in to_find if other_gate.operator == rewritten.operator and len(
                        {other_gate.left, other_gate.right} & {rewritten.left, rewritten.right}) > 0), None)
                    if almost_matches is not None:
                        # The argument not in common with our search pattern is one of our bad outputs:
                        bad_map = ({almost_matches.left, almost_matches.right} - {rewritten.left, rewritten.right}).pop()
                        gate_with_bad_map = next(other_gate for other_gate in to_find if other_gate.output == bad_map)
                        print("  *", gate_with_bad_map)
                        # print(f"{bad1.output} <-> {bad_map}")

                        # print("*", [other_gate for other_gate in to_find if
                        #        other_gate.output in (rewritten.left, rewritten.right) and {other_gate.left, other_gate.right} & {gate_with_bad_map.left, gate_with_bad_map.right}])
                        # print("*2", [other_gate for other_gate in to_find if
                        #             other_gate.output in (rewritten.left, rewritten.right) and {other_gate.left,
                        #                                                                         other_gate.right} & {
                        #                 gate_with_bad_map.left, gate_with_bad_map.right}])
                else:
                    name_mapping[matching_gate.output] = gate.output
                    name_mapping[gate.output] = matching_gate.output

            gates.add(gate)

        for i in range(max_id + 1):
            input_x = f"x{i:02}"
            input_y = f"y{i:02}"
            output_z = f"z{i:02}"
            output_carry = f"carry{i:02}"
            if i == max_id:
                output_carry = f"z{i+1:02}"

            if i == 0:
                add_and_check(Gate(left=input_x, right=input_y, operator="XOR", output=output_z))
                add_and_check(Gate(left=input_x, right=input_y, operator="AND", output=output_carry))
            else:
                xy_xored = f"inputsxored{i:02}"
                xy_anded = f"anded{i:02}"
                cin_anded = f"cinanded{i:02}"
                input_carry = f"carry{i-1:02}"
                add_and_check(Gate(left=input_x, right=input_y, operator="XOR", output=xy_xored))
                add_and_check(Gate(left=input_carry, right=xy_xored, operator="XOR", output=output_z))

                add_and_check(Gate(left=input_x, right=input_y, operator="AND", output=xy_anded))
                add_and_check(Gate(left=input_carry, right=xy_xored, operator="AND", output=cin_anded))
                add_and_check(Gate(left=xy_anded, right=cin_anded, operator="OR", output=output_carry))

        return gates

    def part1(self) -> int:
        return self.evaluate(self.starting_values, self.gates)

    def part2(self) -> str:
        max_input_id = max(int(x_id[1:]) for x_id in self.starting_values if x_id.startswith("x"))
        max_input = (1 << max_input_id) - 1

        custom_gates = self.build_adder_gates(max_input_id, self.gates)
        # TODO: 1. Remove:
        for i in range(1000):
            x = randint(0, max_input)
            y = randint(0, x)
            expected = x + y
            inputs = self.starting_values.copy()
            for i in range(max_input_id + 1):
                inputs[f"x{i:02}"] = (x >> i) & 1
                inputs[f"y{i:02}"] = (y >> i) & 1
            evaluated = self.evaluate(inputs, custom_gates)
            assert expected == evaluated

        return ""

class Day24Example(Day24Base):
    def __init__(self) -> None:
        super().__init__(2024, None, True)

class Day24(Day24Base):
    def __init__(self) -> None:
        super().__init__(69201640933606, "dhq,hbs,jcp,kfp,pdg,z18,z22,z27", False)

if __name__ == "__main__":
    # Day24Example().check()
    Day24().check()
