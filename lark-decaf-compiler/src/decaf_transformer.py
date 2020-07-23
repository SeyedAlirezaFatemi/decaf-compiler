from typing import List, Union

from lark import Transformer, Tree, Token

variable_size = {
    "int": 4,
    "string": 100,
    "double": 8,
    "bool": 4
}


class DecafTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.variable_map = dict()
        self.stack_pointer = 0X7fffffff

    def propagate_rule(self, args):
        print("propagate_rule")
        print(args)
        return args[0]

    def new_variable(self, args):
        variable_type = args[0].children[0]
        variable_name = args[1]

    def new_function(self, args: List[Union[Tree, Token]]):
        print("new_function")
        print(args[2])
        return_type = args[0].children[0]
        function_name = args[1]

    def new_void_function(self, args):
        print("new_void_function")
        print(args)

    def formal_parameters(self, args):
        print("formals")
        print(args)
