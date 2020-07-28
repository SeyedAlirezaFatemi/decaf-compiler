import enum
from dataclasses import dataclass

from .Identifier import Identifier
from .Node import Node


class PrimitiveTypes(enum):
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
