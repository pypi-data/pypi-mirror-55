class Operation(object):
    ADD = '+'
    SUBTRACT = 'sub'
    MULTIPLY = '*'
    DIVIDE = '/'
    PARANTHESES_LEFT = '('
    POWER = '^'
    SQUARE_ROOT = 'sqr'
    MINUS = '-'
    SIN = 'sin'
    COS = 'cos'
    TAN = 'tan'
    SEQ = 'seq'
    CSC = 'csc'
    COT = 'cot'

    def __init__(self, priority, operands_count, handler,):
        self.priority = priority
        self.operands_count = operands_count
        self.handler = handler