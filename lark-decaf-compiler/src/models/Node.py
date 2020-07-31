from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .SymbolTable import SymbolTable
    from .Declaration import Declaration


@dataclass
class Node:
    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        pass


# This model is not used anywhere. At least not yet!
@dataclass
class Program(Node):
    declarations: List[Declaration]
