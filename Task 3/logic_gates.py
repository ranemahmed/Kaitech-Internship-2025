class LogicGate:
    def __init__(self, input1: bool, input2: bool = None):
        self._input1 = input1
        self._input2 = input2

    def output(self) -> bool:
        raise NotImplementedError("Subclasses must override output().")

class ANDGate(LogicGate):
    def output(self) -> bool:
        return self._input1 and self._input2

class ORGate(LogicGate):
    def output(self) -> bool:
        return self._input1 or self._input2

class NOTGate(LogicGate):
    def output(self) -> bool:
        return not self._input1

class XORGate(LogicGate):
    def output(self) -> bool:
        return self._input1 != self._input2

if __name__ == "__main__":
    and_gate = ANDGate(True, False)
    or_gate = ORGate(True, False)
    not_gate = NOTGate(True)
    xor_gate = XORGate(True, False)

    print(f"AND(True, False) = {and_gate.output()}")  # False
    print(f"OR(True, False)  = {or_gate.output()}")   # True
    print(f"NOT(True)        = {not_gate.output()}")   # False
    print(f"XOR(True, False) = {xor_gate.output()}")  # True