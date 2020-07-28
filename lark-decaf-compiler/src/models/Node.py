from dataclasses import dataclass
from typing import List

from .Declaration import Declaration


@dataclass
class Node:
    pass


class Program(Node):
    declarations: List[Declaration]
