from .operations_repository import OperationsRepository


class ReversePolishCalculator(object):

    def __init__(self,):
        self.operations_repository = OperationsRepository()
        self.expression_tokens_queue = []
        self.variable_name = 'x'

    def set_variable_name(self, variable_name):
        self.variable_name = variable_name

    def set_expression_queue(self, expression_tokens_queue):
        self.expression_tokens_queue = expression_tokens_queue

    def compute_at_value(self, x):
        result = None
        operation = ''
        expression_tokens_Copy = self.expression_tokens_queue[:]
        i = 0
        if len(expression_tokens_Copy) == 1 and expression_tokens_Copy[0] not in self.operations_repository.operations:
            operand = expression_tokens_Copy[0]
            if operand == self.variable_name:
                result = x
            elif operand.isdigit():
                result = operand
            else:
                raise Exception('Invalid symbol found')
        else:
            while i < len(expression_tokens_Copy):
                operation = expression_tokens_Copy[i]
                if operation == '(' or operation == ')':
                    raise Exception(
                        'Found open parentheses without closing one or vice versa')
                if operation in self.operations_repository.operations:
                    operand1 = None
                    operand2 = None
                    start_index = -1
                    end_index = -1
                    operation_model = self.operations_repository.operations[operation]
                    operands_count = operation_model.operands_count
                    operation_handler = operation_model.handler

                    if (operands_count == 1):
                        start_index = i - 1
                        end_index = i
                        operand1 = expression_tokens_Copy[i - 1]
                        if operand1 == self.variable_name:
                            operand1 = x
                        result = operation_handler(float(operand1))
                        expression_tokens_Copy = self.update_output_expresions_tokens_with_operation(expression_tokens_Copy, start_index, end_index, result)
                    elif operands_count == 2:
                        if i - 2 < 0:
                            start_index = i - 1
                            end_index = i + 1
                            operand1 = expression_tokens_Copy[i - 1]
                            operand2 = expression_tokens_Copy[i + 1]
                        else:
                            start_index = i - 2
                            end_index = i
                            operand1 = expression_tokens_Copy[i - 2]
                            if operand1 == self.variable_name:
                                operand1 = x

                            operand2 = expression_tokens_Copy[i - 1]
                            if operand2 == self.variable_name:
                                operand2 = x
                            result = operation_handler(float(operand1), float(operand2))
                            expression_tokens_Copy = self.update_output_expresions_tokens_with_operation(
                                expression_tokens_Copy, start_index, end_index, result)
                    i = 0
                else:
                    i += 1
        return result
    
    def update_output_expresions_tokens_with_operation(self, expression_tokens, start_index, end_index, result):
      expression_tokens_Copy = []
      for i in range(len(expression_tokens)):
        if i == start_index:
          expression_tokens_Copy.append(result)
        elif i < start_index or i > end_index:
          expression_tokens_Copy.append(expression_tokens[i])
      return expression_tokens_Copy
  
