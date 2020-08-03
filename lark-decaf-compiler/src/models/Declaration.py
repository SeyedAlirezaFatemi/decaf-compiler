from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Optional

from .Identifier import Identifier
from .Node import Node

if TYPE_CHECKING:
    from .Statement import Statement
    from .Type import Type


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
    function_parameter_offset: int = 0


@dataclass
class FunctionDeclaration(Declaration):
    formal_parameters: List[VariableDeclaration]
    return_type: Type
    body: Statement
    is_method: bool = False
    owner_class: Optional[ClassDeclaration] = None


@dataclass
class ClassDeclaration(Declaration):
    extends: Optional[Identifier]
    variables: List[VariableDeclaration]
    methods: List[FunctionDeclaration]
    instance_size: int = 0
    vtable_size: int = 0

    def find_method_declaration(
        self, method_identifier: Identifier
    ) -> FunctionDeclaration:
        # The optimal solution is to have the methods in a set.
        for method in self.methods:
            if method.identifier.name == method_identifier.name:
                return method
        print(
            f"Error. Method {method_identifier.name} not found in class {self.identifier.name}!"
        )
