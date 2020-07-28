from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from .Node import Node

if TYPE_CHECKING:
    from .Identifier import Identifier


class PrimitiveTypes(Enum):
    INT = "int"
    DOUBLE = "double"
    BOOL = "bool"
    STRING = "string"


@dataclass
class Type(Node):
    name: str


@dataclass
class NamedType(Type):
    identifier: Identifier


@dataclass
class ArrayType(Type):
    elementType: Type
