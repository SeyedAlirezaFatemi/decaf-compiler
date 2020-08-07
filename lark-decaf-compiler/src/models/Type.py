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
    NULL = "null"


PRIMITIVE_TYPES = {"int", "double", "bool", "string"}


@dataclass
class Type(Node):
    name: str

    def is_array(self) -> bool:
        return False

    def __eq__(self, other):
        if isinstance(other, Type):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        elif isinstance(other, PrimitiveTypes):
            return self.name == other.value
        return False


class NamedType(Type):
    identifier: Identifier

    def __init__(self, identifier: Identifier):
        self.name = identifier.name
        self.identifier = identifier


class ArrayType(Type):
    element_type: Type

    def __init__(self, element_type: Type):
        self.name = f"{element_type.name}[]"
        self.element_type = element_type

    def is_array(self) -> bool:
        return True
