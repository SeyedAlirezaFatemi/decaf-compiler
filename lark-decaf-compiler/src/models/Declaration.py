from dataclasses import dataclass
from typing import List

from .Identifier import Identifier
from .Node import Node
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
    members: List[Declaration]
    extends: NamedType
    instance_size: int
    vtable_size: int
    variable_members: List[VariableDeclaration]
    methods: List[FunctionDeclaration]
