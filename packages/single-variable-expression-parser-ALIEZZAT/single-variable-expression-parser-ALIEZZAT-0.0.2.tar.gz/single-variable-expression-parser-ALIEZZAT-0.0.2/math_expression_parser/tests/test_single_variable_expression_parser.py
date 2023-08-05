import unittest
import math

from ..single_variable_parser import SingleVariableParser

class TestSingleVariableParser(unittest.TestCase):
    
    def test_simple_constants_expressions(self):
        parser = SingleVariableParser()
        parser.set_math_function_text('1+1')
        self.assertEqual(parser.compute_function_at_value(0), 2)
    
    def test_complex_constants_expressions(self):
        parser = SingleVariableParser()
        parser.set_math_function_text('sqr((18sub3)/3*(2+3))^2')
        self.assertEqual(parser.compute_function_at_value(0), 25)
    
    def test_trigometric_constant_expression(self):
        parser = SingleVariableParser()
        parser.set_math_function_text('sin(3.14) + cos(0) * tan(0)')
        self.assertLess(parser.compute_function_at_value(0), 1.01)

    def test_trigometric_constant_expression(self):
        parser = SingleVariableParser()
        parser.set_math_function_text('seq(3.14/2) + csc(0) * cot(3.14/2)')
        self.assertLess(parser.compute_function_at_value(0), 1.01)
    
    def test_simple_single_variable_expression(self):
        parser = SingleVariableParser()
        parser.set_math_function_text('x*2+x^2+5')
        self.assertEqual(parser.compute_function_at_value(4), 29)
    
    def test_complex_single_variable_expression(self):
        parser = SingleVariableParser()
        parser.set_math_function_text('sqr((sin(x)*x)^2)')
        self.assertEqual(parser.compute_function_at_value(3.14/2), 1.5699995022029805)

    def test_minus_expression(self):
        parser = SingleVariableParser()
        parser.set_math_function_text('-xsub1')
        self.assertEqual(parser.compute_function_at_value(1), -2)
    
    def test_two_minus_expression(self):
        parser = SingleVariableParser()
        parser.set_math_function_text('-x*-1')
        self.assertEqual(parser.compute_function_at_value(1), 1)

if __name__ == '__main__':
    unittest.main()