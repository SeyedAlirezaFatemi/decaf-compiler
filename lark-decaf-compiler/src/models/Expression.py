from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

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
class InitiateClass(Expression):
    class_identifier: Identifier


@dataclass
class InitiateArray(Expression):
    length_expression: Expression
    element_type: Type
