from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List, Tuple

from .Declaration import ClassDeclaration
from .Identifier import Identifier
from .Node import Node
from .Type import Type, PrimitiveTypes, NamedType, ArrayType

if TYPE_CHECKING:
    from .SymbolTable import SymbolTable
    from typing import TYPE_CHECKING


class Operator(Enum):
    MINUS = "-"
    ADDITION = "+"
    NOT = "!"
    DIVISION = "/"
    MULTIPLICATION = "*"
    MODULO = "%"
    LTE = "<="
    GTE = ">="
    LT = "<"
    GT = ">"
    EQUALS = "=="
    NOT_EQUALS = "!="
    AND = "&&"
    OR = "||"


@dataclass
class Expression(Node):
    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        pass


@dataclass
class BinaryExpression(Expression):
    operator: Operator
    left_expression: Expression
    right_expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        # TODO: based on operators and left and righ expression
        pass


@dataclass
class UnaryExpression(Expression):
    operator: Operator
    expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        # TODO: Is this correct?
        if self.operator == Operator.MINUS:
            return self.expression.evaluate_type(symbol_table)
        elif self.operator == Operator.NOT:
            return Type(PrimitiveTypes.BOOL.value)


@dataclass
class ThisExpression(Expression):
    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        # TODO: Is this correct?
        class_decl = symbol_table.get_current_scope().find_which_class_we_are_in()
        return NamedType(class_decl.identifier.name, class_decl.identifier)


@dataclass
class ReadInteger(Expression):
    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        code = ""
        # TODO: call the _ReadInteger function in standard_library_functions.py
        return code, symbol_table

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return Type(PrimitiveTypes.INT.value)


@dataclass
class ReadLine(Expression):
    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        code = ""
        # TODO: call the _ReadLine function in standard_library_functions.py
        return code, symbol_table

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return Type(PrimitiveTypes.STRING.value)


@dataclass
class LValue(Expression):
    pass


@dataclass
class IdentifierLValue(LValue):
    identifier: Identifier

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.identifier.evaluate_type(symbol_table)


@dataclass
class MemberAccessLValue(LValue):
    expression: Expression
    identifier: Identifier

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        # TODO
        pass


@dataclass
class ArrayAccessLValue(LValue):
    array_expression: Expression
    index_expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        # TODO
        pass


@dataclass
class Assignment(Expression):
    l_value: LValue
    expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        # TODO
        pass


@dataclass
class Call(Expression):
    pass


@dataclass
class FunctionCall(Call):
    function_identifier: Identifier
    actual_parameters: List[Expression]

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.function_identifier.declaration.return_type


@dataclass
class MethodCall(Call):
    class_expression: Expression
    method_identifier: Identifier
    actual_parameters: List[Expression]

    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        code = ""
        # TODO
        # Find class_expression type
        # the method label in assembly will be "_{class_name}_{method_name}"
        # call that function
        return code, symbol_table

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        class_type: NamedType = self.class_expression.evaluate_type(symbol_table)
        class_decl: ClassDeclaration = class_type.identifier.declaration
        method_decl = class_decl.find_method_declaration(self.method_identifier)
        return method_decl.return_type


@dataclass
class InitiateClass(Expression):
    class_identifier: Identifier

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return NamedType(self.class_identifier.name, self.class_identifier)


@dataclass
class InitiateArray(Expression):
    length_expression: Expression
    element_type: Type

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return ArrayType(self.element_type.name, self.element_type)
