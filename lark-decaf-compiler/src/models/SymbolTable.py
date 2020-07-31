from __future__ import annotations

from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Statement import LoopStatement
    from .Declaration import Declaration


class Scope:
    name_declaration_map: Dict[str, Declaration]
    parent_scope: Optional[Scope]
    parent_class_name: Optional[str]
    owner_class_name: Optional[str]

    def __init__(
        self,
        parent_scope: Optional[Scope] = None,
        parent_class_name: Optional[str] = None,
        owner_class_name: Optional[str] = None,
    ):
        self.name_declaration_map = dict()
        self.parent_scope = parent_scope
        self.parent_class_name = parent_class_name
        self.owner_class_name = owner_class_name

    def lookup(self, name):
        if name in self.name_declaration_map:
            return self.name_declaration_map[name]
        if self.parent_scope is None:
            print(f"Error. Variable {name} not found.")
        else:
            return self.parent_scope.lookup(name)

    def add_declaration(self, declaration: Declaration):
        self.name_declaration_map[declaration.identifier.name] = declaration


class SymbolTable:
    global_scope: Scope
    current_scope: Scope
    # This is for keeping track of the loop statements we are inside so we can break out easily
    exterior_loop_statements: List[LoopStatement]

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