from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from .Identifier import Identifier
from .Node import Node

if TYPE_CHECKING:
    from .Statement import Statement
    from .Type import Type, NamedType


@dataclass
class Declaration(Node):
    identifier: Identifier


@dataclass
class VariableDeclaration(Declaration):
    variable_type: Type
    is_global: bool = False
    is_class_member: bool = False
    class_member_offset: int = 0
    is_function_parameter: bool = False


@dataclass
class FunctionDeclaration(Declaration):
    formal_parameters: List[VariableDeclaration]
    return_type: Type
    body: Statement


@dataclass
class ClassDeclaration(Declaration):
    extends: Identifier
    variables: List[VariableDeclaration]
    methods: List[FunctionDeclaration]
    instance_size: int = 0
    vtable_size: int = 0
