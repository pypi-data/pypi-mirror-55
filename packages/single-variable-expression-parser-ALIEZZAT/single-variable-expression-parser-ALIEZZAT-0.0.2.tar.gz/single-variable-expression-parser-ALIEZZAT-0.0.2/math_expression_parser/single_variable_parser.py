import re
from .operations_repository import OperationsRepository
from .reverse_polish_caclulator import ReversePolishCalculator

class SingleVariableParser(object):

    def __init__(self,):
        self.operations_repository = OperationsRepository()
        self.variable_name = 'x'
        self.math_function_text = ''
        self.reverse_polish_calculator = ReversePolishCalculator()
    
    def set_variable_name(self, variable_name):
        self.variable_name = variable_name
    
    def set_math_function_text(self, function_text):    
        if function_text != '':
            self.math_function_text = re.sub(r'\s+', '', function_text)
            self.convert_to_reverese_polish_format()
    
    def compute_function_at_value(self, x):
        if self.math_function_text != '':
            return self.reverse_polish_calculator.compute_at_value(x)

    def convert_to_reverese_polish_format(self):
        if self.math_function_text != '':
            output_queue = []
            operators_stack = []
            operand_value = ''
            i =0
            while i < len(self.math_function_text):
                next_token_to_parse = self.math_function_text[i]
                if (next_token_to_parse in ['c', 'p', 's', 't'] and i + 2 < len(self.math_function_text) and self.math_function_text[i:i+3] in self.operations_repository.operations):
                    next_token_to_parse = self.math_function_text[i: i + 3]
                    i += 2
                #only permit for one dot in number
                if (next_token_to_parse.isdigit() or (next_token_to_parse == '.' and operand_value.find('.') == -1)):
                    if operand_value == '':
                        operand_value = next_token_to_parse
                        if i == len(self.math_function_text) - 1:
                            output_queue.append(operand_value)
                            operand_value = ''
                    else:
                        operand_value += next_token_to_parse
                elif next_token_to_parse == self.variable_name:
                    if operand_value != '':
                        output_queue.append(operand_value)
                        operand_value = ''
                    
                    output_queue.append(self.variable_name)
                else:
                    if (operand_value != ''):
                        output_queue.append(operand_value)
                        operand_value = ''
        
                    operator_to_be_processed = next_token_to_parse

                    if operator_to_be_processed == '(':
                        operators_stack.append(operator_to_be_processed)
                    elif (operator_to_be_processed in self.operations_repository.operations):
                        if len(operators_stack) > 0:
                            while len(operators_stack) > 0:
                                last_operator = operators_stack.pop()
                                last_operation_model = self.operations_repository.operations[last_operator]
                                operation_model_to_be_processed = self.operations_repository.operations[operator_to_be_processed]
                                if last_operation_model.priority >= operation_model_to_be_processed.priority:
                                    output_queue.append(last_operator)
                                else:
                                    operators_stack.append(last_operator)
                                    break
                            operators_stack.append(operator_to_be_processed)
                        else:
                            operators_stack.append(operator_to_be_processed)
                            
                    elif operator_to_be_processed == ')':
                        last_operator = operators_stack.pop()
                        while last_operator != '(':
                            output_queue.append(last_operator)
                            last_operator = operators_stack.pop()
                            if last_operator == None:
                                raise Exception('Found open right parentheses without left one')

                    else:
                        raise Exception('Invalid symbol found')
                i += 1

            while len(operators_stack) > 0:
                last_operator = operators_stack.pop()
                output_queue.append(last_operator)
            self.reverse_polish_calculator.set_expression_queue(output_queue)

