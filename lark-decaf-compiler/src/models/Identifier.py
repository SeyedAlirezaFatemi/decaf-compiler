from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .Node import Node

if TYPE_CHECKING:
    from .Declaration import Declaration


@dataclass
class Identifier(Node):
    name: str
    declaration: Optional[Declaration] = None
    new: bool = False
