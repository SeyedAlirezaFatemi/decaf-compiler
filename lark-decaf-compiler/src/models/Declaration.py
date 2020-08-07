from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Optional

from .Identifier import Identifier
from .Node import Node
from ..utils import calc_variable_size

if TYPE_CHECKING:
    from .Statement import StatementBlock
    from .SymbolTable import SymbolTable
    from .Type import Type


@dataclass
class Declaration(Node):
    identifier: Identifier


@dataclass
class VariableDeclaration(Declaration):
    variable_type: Type
    is_global: bool = False
    global_offset: int = 0
    is_class_member: bool = False
    class_member_offset: int = 0
    is_function_parameter: bool = False
    function_parameter_offset: int = 0
    local_offset: int = 0

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = [f"\t# Code for variable declaration {self.identifier.name}:"]
        current_scope = symbol_table.enter_new_scope()
        current_scope.add_declaration(self)
        if not (self.is_global or self.is_class_member or self.is_function_parameter):
            self.local_offset = symbol_table.get_local_offset()
            symbol_table.increment_local_offset(calc_variable_size(self.variable_type))
            code += [
                f"\tsubu $sp, $sp, {calc_variable_size(self.variable_type)}\t# Decrement sp to make space for variable {self.identifier.name}."
            ]
        code.append(f"\t# End of code for variable declaration {self.identifier.name}.")
        return code


@dataclass
class FunctionDeclaration(Declaration):
    formal_parameters: List[VariableDeclaration]
    return_type: Type
    body: StatementBlock
    is_method: bool = False
    owner_class: Optional[ClassDeclaration] = None
    label: str = "UNSPECIFIED"

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        # Reset local offset for correct local variable addressing
        symbol_table.reset_local_offset()
        if self.owner_class is None:
            self.label = self.identifier.name
        else:
            self.label = (
                f"{self.owner_class.identifier.name}_{self.identifier.name}_meth"
            )
        function_scope = symbol_table.enter_new_scope(self.owner_class)
        for param in self.formal_parameters:
            function_scope.add_declaration(param)
        code = [
            f"{self.label}:",
            "\tsubu $sp, $sp, 8\t# decrement sp to make space to save ra, fp",
            "\tsw $fp, 8($sp)\t# save fp",
            "\tsw $ra, 4($sp)\t# save ra",
            "\taddiu $fp, $sp, 8\t# set up new fp",
        ]
        # TODO: What about objects? What about them?
        code += self.body.generate_code(symbol_table)
        code += [
            "\tmove $sp, $fp\t\t# pop callee frame off stack",
            "\tlw $ra, -4($fp)\t# restore saved ra",
            "\tlw $fp, 0($fp)\t# restore saved fp",
            "\tjr $ra\t\t# return from function",
        ]
        # Reset
        symbol_table.reset_local_offset()
        symbol_table.set_current_scope(function_scope.parent_scope)
        return code


@dataclass
class ClassDeclaration(Declaration):
    extends: Optional[Identifier]
    variables: List[VariableDeclaration]
    methods: List[FunctionDeclaration]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        class_scope = symbol_table.enter_new_scope(owner_class_declaration=self)
        vars_decls = self.all_variables_declarations(symbol_table)
        for var_decl in vars_decls:
            class_scope.add_declaration(var_decl)
        # TODO: methods and parent methods. how do we call them? pass vars?
        code = []
        for method in self.methods:
            code += method.generate_code(symbol_table)
        symbol_table.set_current_scope(class_scope.parent_scope)
        return code

    def calculate_size(self, symbol_table: SymbolTable) -> int:
        vars_decls = self.all_variables_declarations(symbol_table)
        size = 0
        for var_decl in vars_decls:
            size += calc_variable_size(var_decl.variable_type)
        return size

    def all_variables_declarations(
        self, symbol_table: SymbolTable
    ) -> List[VariableDeclaration]:
        parents_decls = self.all_parents_declarations(symbol_table)
        vars_decls = self.variables.copy()
        for parent_decl in parents_decls:
            vars_decls += parent_decl.variables
        class_member_offset = 0
        for var_decl in vars_decls:
            var_decl.class_member_offset = class_member_offset
            class_member_offset += calc_variable_size(var_decl.variable_type)
        return vars_decls

    def all_parents_declarations(
        self, symbol_table: SymbolTable, parents_found: List[ClassDeclaration] = None
    ) -> List[ClassDeclaration]:
        if parents_found is None:
            parents_found = []
        if self.extends is None:
            return parents_found
        parent_decl = self.extends.find_declaration(symbol_table)
        assert isinstance(parent_decl, ClassDeclaration)
        parents_found.append(parent_decl)
        return parent_decl.all_parents_declarations(symbol_table, parents_found)

    def find_variable_declaration(
        self, symbol_table: SymbolTable, variable_identifier: Identifier
    ) -> VariableDeclaration:
        # The optimal solution is to have the methods in a set.
        for var_decl in self.all_variables_declarations(symbol_table):
            if var_decl.identifier.name == variable_identifier.name:
                return var_decl
        print(
            f"Error. Method {variable_identifier.name} not found in class {self.identifier.name}!"
        )

    def find_method_declaration(
        self, symbol_table: SymbolTable, method_identifier: Identifier
    ) -> FunctionDeclaration:
        # The optimal solution is to have the methods in a set.
        for method in self.methods:
            if method.identifier.name == method_identifier.name:
                return method
        parents_decls = self.all_parents_declarations(symbol_table)
        if len(parents_decls):
            print(
                f"Error. Method {method_identifier.name} not found in class {self.identifier.name}!"
            )
        return parents_decls[0].find_method_declaration(symbol_table, method_identifier)
