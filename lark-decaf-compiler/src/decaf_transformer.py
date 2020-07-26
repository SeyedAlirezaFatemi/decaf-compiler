from dataclasses import dataclass
from typing import List, Union, Any, Optional

from lark import Transformer, Tree, Token

variable_size = {"int": 4, "string": 100, "double": 8, "bool": 4}


@dataclass
class Variable:
    name: str
    type: str


@dataclass
class NodeOutput:
    code: str
    address: Any


class DecafTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.variable_map = dict()
        self.stack_pointer = 0x7FFFFFFF

    def pass_up(self, args):
        return args

    def pass_up_first_element(self, args):
        return args[0]

    def new_variable(self, args):
        # Here, we should take space for the variable and insert it to the spaghetti stack
        print("new_variable")
        print(args)
        return args[0]

    def variable_definition(self, args):
        print("variable_definition", args)
        variable_type = args[0]
        variable_name = args[1]
        return Variable(variable_name, variable_type)

    def new_function(self, args: List[Union[Tree, Token]]):
        print("new_function")
        print(args)
        return_type = args[0]
        function_name = args[1]
        function_parameters = args[2]

    def new_void_function(self, args):
        print("new_void_function")
        print(args)
        function_name = args[0]
        function_parameters = args[1]

    def new_class(self, args):
        print("new_class")
        print(args)
        class_name = args[0]

    def new_interface(self, args):
        print("new_interface")
        print(args)

    def finalize(self, args):
        pass

    def print(self, args):
        """
        Page A-49
        Code is inside standard_library_functions.py
        print_int 01 $a0 = integer
        print_float 02 $f12 = float
        print_double 03 $f12 = double
        print_string 04 $a0 = string
        """
        # TODO: Call
        pass

    def read_integer(self, args):
        """
        Page A-49
        Code is inside standard_library_functions.py
        read_int 05 integer (in $v0)
        """
        # TODO: Call
        pass


class SymbolTable:
    pass


class Scope:
    pass


class CodeGenerator:
    def generate_code(self, scope: Scope) -> str:
        pass


class Expression(CodeGenerator):
    pass


class Statement(CodeGenerator):
    pass


class IfStatement(Statement):
    condition_expression: Expression
    true_statement: Statement
    false_statement: Statement


class WhileStatement(Statement):
    condition_expression: Expression
    true_statement: Statement
    false_statement: Statement


class ReturnStatement(Statement):
    return_expression: Optional[Expression]


class PrintStatement(Statement):
    expressions: List[Expression]


class ForStatement(Statement):
    initialization_expression: Optional[Expression]
    condition_expression: Expression
    update_expression: Optional[Expression]
    statement: Statement

    def generate_code(self, scope) -> str:
        code = "_L2:\n"
        code += self.initialization_expression.generate_code(scope)
        code += self.condition_expression.generate_code(scope)
        code += self.statement.generate_code(scope)
        return code


class BreakStatement(Statement):
    pass
