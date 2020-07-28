from typing import Dict, Optional

from .Declaration import Declaration


class Scope:
    name_declaration_map: Dict[str, Declaration]
    parent_scope: Optional["Scope"]
    parent_class_name: Optional[str]
    owner_class_name: Optional[str]

    def __init__(
        self,
        parent_scope: Optional["Scope"] = None,
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
            print("Error")
        else:
            return self.parent_scope.lookup(name)

    def add_declaration(self, declaration: Declaration):
        self.name_declaration_map[declaration.identifier.name] = declaration


class SymbolTable:
    global_scope: Scope
    current_scope: Scope

    def __init__(self):
        # init global scope
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def enter_new_scope(self, owner_class_name: Optional[str] = None):
        new_scope = Scope(self.current_scope, owner_class_name=owner_class_name)
        self.current_scope = new_scope

    def exit_current_scope(self):
        prev_scope = self.current_scope
        self.current_scope = self.current_scope.parent_scope
        del prev_scope

    def add_declaration_to_global_scope(self, declaration: Declaration):
        self.global_scope.add_declaration(declaration)

    def add_declaration_to_current_scope(self, declaration: Declaration):
        self.current_scope.add_declaration(declaration)
