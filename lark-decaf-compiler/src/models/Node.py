from __future__ import annotations

from dataclasses import dataclass
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Declaration import Declaration


@dataclass
class Node:
    pass


@dataclass
class Program(Node):
    declarations: List[Declaration]
