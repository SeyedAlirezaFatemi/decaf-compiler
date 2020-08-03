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

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        from .Declaration import VariableDeclaration

        if isinstance(self.declaration, VariableDeclaration):
            return self.declaration.variable_type
        # Well...
        # What about the others?
