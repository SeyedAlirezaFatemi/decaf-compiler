from typing import List, Union

from lark import Transformer, Tree, Token

from models.Declaration import FunctionDeclaration, VariableDeclaration
from models.Type import Type

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

    def new_variable(self, args):
        print("new_variable")
        variable_declaration: VariableDeclaration = args[0]
        variable_declaration.is_function_parameter = False
        return variable_declaration

    def variable_definition(self, args):
        print("variable_definition", args)
        variable_type, variable_identifier = args[0]
        return VariableDeclaration(variable_identifier, variable_type)

    def new_function(self, args: List[Union[Tree, Token]]):
        print("new_function")
        print(args)
        return_type, function_identifier, function_parameters, function_body = args
        return FunctionDeclaration(
            function_identifier, function_parameters, return_type, function_body
        )

    def new_void_function(self, args):
        print("new_void_function")
        print(args)
        function_identifier, function_parameters, function_body = args
        return FunctionDeclaration(
            function_identifier, function_parameters, Type("void"), function_body
        )

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
