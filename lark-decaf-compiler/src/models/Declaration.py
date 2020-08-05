from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Optional

from .Identifier import Identifier
from .Node import Node

if TYPE_CHECKING:
    from .Statement import Statement
    from .SymbolTable import SymbolTable
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

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        current_scope = symbol_table.enter_new_scope()
        current_scope.add_declaration(self)
        # TODO: Do we need to generate code?
        return []


@dataclass
class FunctionDeclaration(Declaration):
    formal_parameters: List[VariableDeclaration]
    return_type: Type
    body: Statement
    is_method: bool = False
    owner_class: Optional[ClassDeclaration] = None
    label: str = "UNSPECIFIED"

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        if self.owner_class is None:
            self.label = f"{self.identifier.name}_func"
        else:
            self.label = (
                f"{self.owner_class.identifier.name}_{self.identifier.name}_meth"
            )

        # TODO: add formal parameters to symbol table and generate code

        return code


@dataclass
class ClassDeclaration(Declaration):
    extends: Optional[Identifier]
    variables: List[VariableDeclaration]
    methods: List[FunctionDeclaration]
    instance_size: int = 0
    vtable_size: int = 0

    def find_variable_declaration(
        self, variable_identifier: Identifier
    ) -> VariableDeclaration:
        # The optimal solution is to have the methods in a set.
        for variable in self.variables:
            if variable.identifier.name == variable_identifier.name:
                return variable
        print(
            f"Error. Method {variable_identifier.name} not found in class {self.identifier.name}!"
        )

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
