from __future__ import annotations

from typing import TYPE_CHECKING

from .Node import Node

if TYPE_CHECKING:
    from .Declaration import Declaration


class Identifier(Node):
    name: str
    declarations: Declaration
