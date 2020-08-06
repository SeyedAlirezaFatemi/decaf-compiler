from __future__ import annotations

from typing import Dict, Optional, List, TYPE_CHECKING

from ..utils import calc_variable_size

if TYPE_CHECKING:
    from .Statement import LoopStatement
    from .Declaration import Declaration, ClassDeclaration


class Scope:
    name_declaration_map: Dict[str, Declaration]
    parent_scope: Optional[Scope]
    owner_class_declaration: Optional[ClassDeclaration]

    def __init__(
        self,
        parent_scope: Optional[Scope] = None,
        owner_class_declaration: Optional[ClassDeclaration] = None,
    ):
        self.name_declaration_map = dict()
        self.parent_scope = parent_scope
        self.owner_class_declaration = owner_class_declaration

    def lookup(self, name) -> Declaration:
        if name in self.name_declaration_map:
            return self.name_declaration_map[name]
        if self.parent_scope is None:
            print(f"Error. Variable {name} not found.")
        else:
            return self.parent_scope.lookup(name)

    def add_declaration(self, declaration: Declaration):
        self.name_declaration_map[declaration.identifier.name] = declaration

    def find_which_class_we_are_in(self) -> ClassDeclaration:
        if self.owner_class_declaration is not None:
            return self.owner_class_declaration
        elif self.parent_scope is not None:
            return self.parent_scope.find_which_class_we_are_in()
        print("Error. You are not inside a class.")


class SymbolTable:
    global_scope: Scope
    current_scope: Scope
    # This is for keeping track of the loop statements we are inside so we can break out easily
    exterior_loop_statements: List[LoopStatement] = []
    for_number: int = 0
    while_number: int = 0
    else_number: int = 0
    if_number: int = 0
    local_offset: int = 0

    def __init__(self):
        # init global scope
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def enter_loop(self, loop_statement: LoopStatement):
        self.exterior_loop_statements.append(loop_statement)

    def exit_loop(self) -> LoopStatement:
        return self.exterior_loop_statements.pop()

    def get_current_loop_statement(self) -> LoopStatement:
        return self.exterior_loop_statements[-1]

    def get_current_scope(self) -> Scope:
        return self.current_scope

    def get_global_scope(self) -> Scope:
        return self.global_scope

    def set_current_scope(self, scope: Scope):
        self.current_scope = scope

    def enter_new_scope(
        self, owner_class_declaration: Optional[ClassDeclaration] = None
    ) -> Scope:
        new_scope = Scope(self.current_scope, owner_class_declaration)
        self.current_scope = new_scope
        return new_scope

    def exit_current_scope(self) -> Scope:
        prev_scope = self.current_scope
        self.current_scope = self.current_scope.parent_scope
        del prev_scope
        return self.current_scope

    def add_declaration_to_global_scope(self, declaration: Declaration):
        self.global_scope.add_declaration(declaration)

    def add_declaration_to_current_scope(self, declaration: Declaration):
        self.current_scope.add_declaration(declaration)

    def get_current_while_number(self) -> int:
        self.while_number += 1
        return self.while_number

    def get_current_for_number(self) -> int:
        self.for_number += 1
        return self.for_number

    def get_current_if_number(self) -> int:
        self.if_number += 1
        return self.if_number

    def get_current_else_number(self) -> int:
        self.else_number += 1
        return self.else_number

    def reset_local_offset(self):
        self.local_offset = 0

    def increment_local_offset(self, amount: int):
        self.local_offset += amount

    def decrement_local_offset(self, amount: int):
        # Pop
        self.local_offset -= amount

    def get_local_offset(self) -> int:
        return self.local_offset

    def pop_variables_till_block(
        self, scope: Scope, block_scope: Scope, popped_size_till_now: int = 0
    ) -> int:
        from .Declaration import VariableDeclaration
        if scope == block_scope:
            return popped_size_till_now
        for decl in scope.name_declaration_map.values():
            assert isinstance(decl, VariableDeclaration)
            # Pop variables
            size = calc_variable_size(decl.variable_type)
            self.decrement_local_offset(size)
            popped_size_till_now += size
        self.pop_variables_till_block(
            scope.parent_scope, block_scope, popped_size_till_now
        )
