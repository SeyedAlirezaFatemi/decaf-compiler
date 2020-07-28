from lark import Transformer

from .models.Declaration import FunctionDeclaration, VariableDeclaration
from .models.Identifier import Identifier
from .models.Statement import BreakStatement, ReturnStatement
from .models.Type import Type

variable_size = {"int": 4, "string": 100, "double": 8, "bool": 4}


class DecafTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.variable_map = dict()
        self.stack_pointer = 0x7FFFFFFF

    def pass_up(self, args):
        return args

    def pass_up_first_element(self, args):
        return args[0]

    def new_identifier(self, args):
        identifier_name = args[0]
        return Identifier(identifier_name, new=True)

    def identifier(self, args):
        identifier_name = args[0]
        return Identifier(identifier_name, new=False)

    def new_variable(self, args):
        print("new_variable")
        variable_declaration: VariableDeclaration = args[0]
        variable_declaration.is_function_parameter = (
            False
        )  # Still may be global or class member
        return variable_declaration

    def variable_definition(self, args):
        print("variable_definition", args)
        variable_type, variable_identifier = args
        variable_declaration = VariableDeclaration(variable_identifier, variable_type)
        variable_identifier.declaration = variable_declaration
        return variable_declaration

    def new_function(self, args):
        print("new_function")
        print(args)
        return_type, function_identifier, function_parameters, function_body = args
        function_declaration = FunctionDeclaration(
            function_identifier, function_parameters, return_type, function_body
        )
        function_identifier.declaration = function_declaration
        return function_declaration

    def new_void_function(self, args):
        print("new_void_function")
        print(args)
        function_identifier, function_parameters, function_body = args
        function_declaration = FunctionDeclaration(
            function_identifier, function_parameters, Type("void"), function_body
        )
        function_identifier.declaration = function_declaration
        return function_declaration

    def new_class(self, args):
        print("new_class")
        print(args)
        class_name = args[0]

    def break_statement(self, args):
        return BreakStatement()

    def return_statement(self, args):
        return_expression = args[0]
        return ReturnStatement(return_expression)

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
