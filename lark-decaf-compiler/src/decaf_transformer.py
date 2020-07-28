from lark import Transformer

from .models.Declaration import (
    FunctionDeclaration,
    VariableDeclaration,
    ClassDeclaration,
)
from .models.Expression import (
    ReadInteger,
    ReadLine,
    ThisExpression,
    UnaryExpression,
    BinaryExpression, IdentifierLValue, MemberAccessLValue, ArrayAccessLValue, Assignment,
)
from .models.Identifier import Identifier
from .models.Statement import (
    BreakStatement,
    ReturnStatement,
    IfStatement,
    WhileStatement,
    ForStatement,
    PrintStatement,
)
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
        if len(args) == 0:
            return None
        return args[0]

    def new_identifier(self, args):
        identifier_name = args[0]
        return Identifier(identifier_name, new=True)

    def identifier(self, args):
        identifier_name = args[0]
        return Identifier(identifier_name, new=False)

    def new_variable(self, args):
        variable_declaration: VariableDeclaration = args[0]
        variable_declaration.is_function_parameter = (
            False
        )  # Still may be global or class member
        return variable_declaration

    def variable_definition(self, args):
        variable_type, variable_identifier = args
        variable_declaration = VariableDeclaration(variable_identifier, variable_type)
        variable_identifier.declaration = variable_declaration
        return variable_declaration

    def new_function(self, args):
        return_type, function_identifier, function_parameters, function_body = args
        function_declaration = FunctionDeclaration(
            function_identifier, function_parameters, return_type, function_body
        )
        function_identifier.declaration = function_declaration
        return function_declaration

    def new_void_function(self, args):
        function_identifier, function_parameters, function_body = args
        function_declaration = FunctionDeclaration(
            function_identifier, function_parameters, Type("void"), function_body
        )
        function_identifier.declaration = function_declaration
        return function_declaration

    def new_class(self, args):
        print("new_class")
        print(args)
        class_identifier, extend_identifier, implement_identifiers, fields_declarations = (
            args
        )
        # Extract these from field declarations
        variable_declarations = []
        function_declarations = []
        class_declaration = ClassDeclaration(
            class_identifier,
            extend_identifier,
            variable_declarations,
            function_declarations,
        )
        class_identifier.declaration = class_declaration
        return class_declaration

    def if_statement(self, args):
        else_body_statement = None
        if len(args) == 3:
            condition_expression, body_statement, else_body_statement = args
        else:
            condition_expression, body_statement = args
        return IfStatement(condition_expression, body_statement, else_body_statement)

    def while_statement(self, args):
        condition_expression, body_statement = args
        return WhileStatement(condition_expression, body_statement)

    def for_statement(self, args):
        initialization_expression, condition_expression, update_expression, body_statement = (
            args
        )
        return ForStatement(
            initialization_expression,
            condition_expression,
            update_expression,
            body_statement,
        )

    def break_statement(self, args):
        return BreakStatement()

    def return_statement(self, args):
        return_expression = args[0]
        return ReturnStatement(return_expression)

    def print_statement(self, args):
        """
        Page A-49
        Code is inside standard_library_functions.py
        print_int 01 $a0 = integer
        print_float 02 $f12 = float
        print_double 03 $f12 = double
        print_string 04 $a0 = string
        """
        return PrintStatement(args)

    def this_expression(self, args):
        return ThisExpression()

    def unary_operation(self, args):
        operator, expression = args
        return UnaryExpression(operator, expression)

    def binary_operation(self, args):
        left_expression, operator, right_expression = args
        return BinaryExpression(operator, left_expression, right_expression)

    def identifier_l_value(self, args):
        identifier = args[0]
        return IdentifierLValue(identifier)

    def member_access_l_value(self, args):
        expression, identifier = args
        return MemberAccessLValue(expression, identifier)

    def array_access_l_value(self, args):
        array_expression, index_expression = args
        return ArrayAccessLValue(array_expression, index_expression)

    def assignment(self, args):
        l_value, expression = args
        return Assignment(l_value, expression)

    def read_integer(self, args):
        """
        Page A-49
        Code is inside standard_library_functions.py
        read_int 05 integer (in $v0)
        """
        return ReadInteger()

    def read_line(self, args):
        return ReadLine()

    def finalize(self, args):
        print(args)
        pass
