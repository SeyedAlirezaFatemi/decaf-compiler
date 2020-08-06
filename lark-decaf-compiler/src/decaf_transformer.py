from typing import List

from lark import Transformer

from .models.Declaration import (
    FunctionDeclaration,
    VariableDeclaration,
    ClassDeclaration,
    Declaration,
)
from .models.Expression import (
    ReadInteger,
    ReadLine,
    ThisExpression,
    UnaryExpression,
    BinaryExpression,
    IdentifierLValue,
    MemberAccessLValue,
    ArrayAccessLValue,
    Assignment,
    FunctionCall,
    MethodCall,
    Operator, Constant,
)
from .models.Identifier import Identifier
from .models.Statement import (
    BreakStatement,
    ReturnStatement,
    IfStatement,
    WhileStatement,
    ForStatement,
    PrintStatement,
    StatementBlock,
    OptionalExpressionStatement,
    Statement,
)
from .models.SymbolTable import SymbolTable
from .models.Type import Type, ArrayType, NamedType, PrimitiveTypes
from .utils import calc_variable_size

variable_size = {"int": 4, "string": 100, "double": 8, "bool": 4}
stack_pointer = 0x7FFFFFFF


class DecafTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def pass_up(self, args):
        return args

    def pass_up_first_element(self, args):
        if len(args) == 0:
            return None
        return args[0]

    def array_type(self, args):
        element_type = args[0]
        return ArrayType(element_type.name, element_type)

    def named_type(self, args):
        identifier = args[0]
        return NamedType(identifier.name, identifier)

    def prim_type(self, args):
        prim = args[0]
        return Type(prim)

    def int_const(self, args):
        return Constant(Type(PrimitiveTypes.INT.value), args[0])

    def double_const(self, args):
        return Constant(Type(PrimitiveTypes.DOUBLE.value), args[0])

    def string_const(self, args):
        return Constant(Type(PrimitiveTypes.STRING.value), args[0])

    def bool_const(self, args):
        return Constant(Type(PrimitiveTypes.BOOL.value), args[0])

    def null_const(self, args):
        return Constant(Type(PrimitiveTypes.NULL.value), args[0])

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
        function_identifier.new = True
        offset = 0
        for idx, formal_parameter in enumerate(function_declaration.formal_parameters):
            formal_parameter.is_function_parameter = True
            formal_parameter.function_parameter_offset = offset
            offset += calc_variable_size(formal_parameter.variable_type)
        return function_declaration

    def new_void_function(self, args):
        function_identifier, function_parameters, function_body = args
        function_declaration = FunctionDeclaration(
            function_identifier, function_parameters, Type("void"), function_body
        )
        function_identifier.declaration = function_declaration
        function_identifier.new = True
        offset = 0
        for idx, formal_parameter in enumerate(function_declaration.formal_parameters):
            formal_parameter.is_function_parameter = True
            formal_parameter.function_parameter_offset = offset
            offset += calc_variable_size(formal_parameter.variable_type)
        return function_declaration

    def new_class(self, args):
        class_identifier, extend_identifier, implement_identifiers, fields_declarations = (
            args
        )
        # Extract these from field declarations
        variable_declarations = []
        method_declarations = []
        class_member_offset = 0
        class_size = 0
        for field in fields_declarations:
            if isinstance(field, VariableDeclaration):
                variable_declarations.append(field)
                field.is_class_member = True
                field.class_member_offset = class_member_offset
                class_member_offset += calc_variable_size(field.variable_type)
                class_size += calc_variable_size(field.variable_type)
            else:
                method_declarations.append(field)
                field.is_method = True
        class_declaration = ClassDeclaration(
            class_identifier,
            extend_identifier,
            variable_declarations,
            method_declarations,
            instance_size=class_size,
        )
        for method in method_declarations:
            method.owner_class = class_declaration
        class_identifier.declaration = class_declaration
        class_identifier.new = True
        return class_declaration

    def statement_block(self, args):
        variable_declarations, statements = [], []
        for arg in args:
            if type(arg) == Statement:
                statements.append(arg)
            else:
                variable_declarations.append(arg)
        return StatementBlock(variable_declarations, statements)

    def optional_expresion_statement(self, args):
        return OptionalExpressionStatement(args[0])

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

    def minus_operation(self, args):
        expression = args
        return UnaryExpression(Operator.MINUS, expression)

    def not_operation(self, args):
        expression = args
        return UnaryExpression(Operator.NOT, expression)

    def multiplication_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(
            Operator.MULTIPLICATION, left_expression, right_expression
        )

    def addition_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.ADDITION, left_expression, right_expression)

    def subtraction_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.MINUS, left_expression, right_expression)

    def modulo_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.MODULO, left_expression, right_expression)

    def division_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.DIVISION, left_expression, right_expression)

    def lt_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.LT, left_expression, right_expression)

    def lte_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.LTE, left_expression, right_expression)

    def gt_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.GT, left_expression, right_expression)

    def gte_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.GTE, left_expression, right_expression)

    def equals_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.EQUALS, left_expression, right_expression)

    def not_equals_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.NOT_EQUALS, left_expression, right_expression)

    def and_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.AND, left_expression, right_expression)

    def or_operation(self, args):
        left_expression, right_expression = args
        return BinaryExpression(Operator.OR, left_expression, right_expression)

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

    def function_call(self, args):
        function_identifier, actual_parameters = args
        return FunctionCall(function_identifier, actual_parameters)

    def method_call(self, args):
        print(args)
        class_expression, method_identifier, actual_parameters = args
        return MethodCall(class_expression, method_identifier, actual_parameters)

    def read_integer(self, args):
        """
        Page A-49
        Code is inside standard_library_functions.py
        read_int 05 integer (in $v0)
        """
        return ReadInteger()

    def read_line(self, args):
        return ReadLine()

    def finalize(self, args: List[Declaration]):
        symbol_table = SymbolTable()
        # First Pass
        # Initialize global scope
        variable_global_offset = 0
        for arg in args:
            symbol_table.add_declaration_to_global_scope(arg)
            if isinstance(arg, VariableDeclaration):
                arg.is_global = True
                arg.global_offset = variable_global_offset
                variable_type = arg.variable_type
                variable_global_offset += calc_variable_size(variable_type)
        # Second Pass
        # Generate code
        code = []
        for arg in args:
            code_part = arg.generate_code(symbol_table)
            code += code_part
        # Write on file
        # TODO
        print(code)
