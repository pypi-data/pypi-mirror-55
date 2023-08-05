from .models.operation import Operation
import math

class OperationsRepository(object):
    def __init__(self):
        self.operations = {}
        self.operations[Operation.ADD] = Operation(1, 2, lambda x, y : x + y)
        self.operations[Operation.SUBTRACT] = Operation(1, 2, lambda x, y : x - y)
        self.operations[Operation.MULTIPLY] = Operation(2, 2, lambda x, y : x * y)
        self.operations[Operation.DIVIDE] = Operation(2, 2, lambda x, y : x / y)
        self.operations[Operation.PARANTHESES_LEFT] = Operation(0, 0, None)
        self.operations[Operation.POWER] = Operation(7, 2, lambda x, y : x ** y)
        self.operations[Operation.SQUARE_ROOT] = Operation(7, 1, lambda x : math.sqrt(x))
        self.operations[Operation.MINUS] = Operation(6, 1, lambda x : x*-1)
        self.operations[Operation.SIN] = Operation(7, 1, lambda x : math.sin(x))
        self.operations[Operation.COS] = Operation(7, 1, lambda x : math.cos(x))
        self.operations[Operation.TAN] = Operation(7, 1, lambda x : math.tan(x))
        self.operations[Operation.SEQ] = Operation(7, 1, lambda x : 1 / math.sin(x))
        self.operations[Operation.CSC] = Operation(7, 1, lambda x : 1 / math.cos(x))
        self.operations[Operation.COT] = Operation(7, 1, lambda x : 1 / math.tan(x))