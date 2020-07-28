from .Declaration import Declaration
from .Node import Node


class Identifier(Node):
    name: str
    declarations: Declaration
