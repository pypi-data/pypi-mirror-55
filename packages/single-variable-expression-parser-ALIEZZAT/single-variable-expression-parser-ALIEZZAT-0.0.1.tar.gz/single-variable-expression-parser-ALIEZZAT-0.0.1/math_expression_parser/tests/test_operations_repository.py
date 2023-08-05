import unittest
from ..models.operation import Operation
from ..operations_repository import OperationsRepository

class TestOperaionsRepository(unittest.TestCase):
    
    def test_add_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.ADD]
        self.assertEqual(operation_model.priority, 1)
        self.assertEqual(operation_model.operands_count, 2)
        self.assertEqual(operation_model.handler(4,2), 6)
    
    def test_subtraction_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.SUBTRACT]
        self.assertEqual(operation_model.priority, 1)
        self.assertEqual(operation_model.operands_count, 2)
        self.assertEqual(operation_model.handler(2,4), -2)
    
    def test_multiplication_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.MULTIPLY]
        self.assertEqual(operation_model.priority, 2)
        self.assertEqual(operation_model.operands_count, 2)
        self.assertEqual(operation_model.handler(6,3), 18)
    
    def test_division_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.DIVIDE]
        self.assertEqual(operation_model.priority, 2)
        self.assertEqual(operation_model.operands_count, 2)
        self.assertEqual(operation_model.handler(9,3), 3)
    
    def test_parantheses_left_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.PARANTHESES_LEFT]
        self.assertEqual(operation_model.priority, 0)
        self.assertEqual(operation_model.operands_count, 0)
        self.assertEqual(operation_model.handler, None)
    
    def test_power_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.POWER]
        self.assertEqual(operation_model.priority, 7)
        self.assertEqual(operation_model.operands_count, 2)
        self.assertEqual(operation_model.handler(2,10), 1024)
    
    def test_square_root_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.SQUARE_ROOT]
        self.assertEqual(operation_model.priority, 7)
        self.assertEqual(operation_model.operands_count, 1)
        self.assertEqual(operation_model.handler(16), 4)
    
    def test_minus_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.MINUS]
        self.assertEqual(operation_model.priority, 6)
        self.assertEqual(operation_model.operands_count, 1)
        self.assertEqual(operation_model.handler(7), -7)

    def test_sin_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.SIN]
        self.assertEqual(operation_model.priority, 7)
        self.assertEqual(operation_model.operands_count, 1)
        self.assertEqual(operation_model.handler(0), 0)
    
    def test_cos_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.COS]
        self.assertEqual(operation_model.priority, 7)
        self.assertEqual(operation_model.operands_count, 1)
        self.assertEqual(operation_model.handler(0), 1)
    
    def test_tan_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.TAN]
        self.assertEqual(operation_model.priority, 7)
        self.assertEqual(operation_model.operands_count, 1)
        self.assertEqual(operation_model.handler(0), 0)
    
    def test_seq_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.SEQ]
        self.assertEqual(operation_model.priority, 7)
        self.assertEqual(operation_model.operands_count, 1)
        with self.assertRaises(ZeroDivisionError):
            operation_model.handler(0)

    def test_csc_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.CSC]
        self.assertEqual(operation_model.priority, 7)
        self.assertEqual(operation_model.operands_count, 1)
        self.assertEqual(operation_model.handler(0), 1)
    
    def test_cot_operation(self):
        operations_repo = OperationsRepository()
        operation_model = operations_repo.operations[Operation.COT]
        self.assertEqual(operation_model.priority, 7)
        self.assertEqual(operation_model.operands_count, 1)
        with self.assertRaises(ZeroDivisionError):
            operation_model.handler(0)

if __name__ == '__main__':
    unittest.main()