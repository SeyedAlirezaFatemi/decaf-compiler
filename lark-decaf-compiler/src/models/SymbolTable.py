from __future__ import annotations

from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Statement import LoopStatement
    from .Declaration import Declaration, ClassDeclaration


class Scope:
    name_declaration_map: Dict[str, Declaration]
    parent_scope: Optional[Scope]
    owner_class_name: Optional[str]
    parent_class_name: Optional[str]

    def __init__(
        self,
        parent_scope: Optional[Scope] = None,
        owner_class_name: Optional[str] = None,
        parent_class_name: Optional[str] = None,
    ):
        self.name_declaration_map = dict()
        self.parent_scope = parent_scope
        self.parent_class_name = parent_class_name
        self.owner_class_name = owner_class_name

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
        if self.owner_class_name is not None:
            return self.lookup(self.owner_class_name)
        if self.parent_scope is None:
            print("Error")
        return self.parent_scope.find_which_class_we_are_in()


class SymbolTable:
    global_scope: Scope
    current_scope: Scope
    # This is for keeping track of the loop statements we are inside so we can break out easily
    exterior_loop_statements: List[LoopStatement]
    for_number: int = 0
    while_number: int = 0
    else_number: int = 0
    if_number: int = 0

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

    def enter_new_scope(self, owner_class_name: Optional[str] = None) -> Scope:
        new_scope = Scope(self.current_scope, owner_class_name=owner_class_name)
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
