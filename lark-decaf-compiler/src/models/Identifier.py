from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .Node import Node
from .SymbolTable import SymbolTable

if TYPE_CHECKING:
    from .Declaration import Declaration
    from .Type import Type


@dataclass
class Identifier(Node):
    name: str
    declaration: Optional[Declaration] = None
    new: bool = False

    def find_declaration(self, symbol_table: SymbolTable) -> Declaration:
        return symbol_table.get_current_scope().lookup(self.name)

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        from .Declaration import VariableDeclaration

        if self.declaration is not None and isinstance(self.declaration, VariableDeclaration):
            return self.declaration.variable_type
        decl = self.find_declaration(symbol_table)
        if isinstance(decl, VariableDeclaration):
            return decl.variable_type
        # Well...
        # What about the others?
