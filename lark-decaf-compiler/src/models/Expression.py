from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List

from .Identifier import Identifier
from .Node import Node
from .Type import Type

if TYPE_CHECKING:
    from typing import TYPE_CHECKING


class Operator(Enum):
    MINUS = "-"
    PLUS = "+"
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
    pass


@dataclass
class BinaryExpression(Expression):
    operator: Operator
    left_expression: Expression
    right_expression: Expression


@dataclass
class UnaryExpression(Expression):
    operator: Operator
    expression: Expression


@dataclass
class ThisExpression(Expression):
    pass


@dataclass
class ReadInteger(Expression):
    pass


@dataclass
class ReadLine(Expression):
    pass


@dataclass
class LValue(Expression):
    pass


@dataclass
class IdentifierLValue(LValue):
    identifier: Identifier


@dataclass
class MemberAccessLValue(LValue):
    expression: Expression
    identifier: Identifier


@dataclass
class ArrayAccessLValue(LValue):
    array_expression: Expression
    index_expression: Expression


@dataclass
class Assignment(Expression):
    l_value: LValue
    expression: Expression


@dataclass
class Call(Expression):
    pass


@dataclass
class FunctionCall(Call):
    function_identifier: Identifier
    actual_parameters: List[Expression]


@dataclass
class MethodCall(Call):
    class_expression: Expression
    method_identifier: Identifier
    actual_parameters: List[Expression]


@dataclass
class InitiateClass(Expression):
    class_identifier: Identifier


@dataclass
class InitiateArray(Expression):
    length_expression: Expression
    element_type: Type
