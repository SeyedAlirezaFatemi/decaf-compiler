from dataclasses import dataclass
from typing import List, Union

from lark import Transformer, Tree, Token

variable_size = {
    "int": 4,
    "string": 100,
    "double": 8,
    "bool": 4
}


@dataclass
class Variable:
    name: str
    type: str


class DecafTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.variable_map = dict()
        self.stack_pointer = 0X7fffffff

    def pass_up(self, args):
        print("pass_up")
        print(args)
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

    def formal_parameters(self, args):
        return args
