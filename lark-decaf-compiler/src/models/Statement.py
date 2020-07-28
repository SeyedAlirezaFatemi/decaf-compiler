from dataclasses import dataclass
from typing import List, Optional

from .Declaration import VariableDeclaration
from .Expression import Expression
from .Node import Node


@dataclass
class Statement(Node):
    pass


@dataclass
class StatementBlock(Statement):
    variable_declarations: List[VariableDeclaration]
    statements: List[Statement]


@dataclass
class IfStatement(Statement):
    condition_expression: Expression
    body_statement: Statement
    else_body_statement: Statement


@dataclass
class WhileStatement(Statement):
    condition_expression: Expression
    body_statement: Statement
    end_label: str


@dataclass
class ReturnStatement(Statement):
    return_expression: Optional[Expression]


@dataclass
class PrintStatement(Statement):
    args: List[Expression]


@dataclass
class ForStatement(Statement):
    initialization_expression: Optional[Expression]
    condition_expression: Expression
    update_expression: Optional[Expression]
    body_statement: Statement
    end_label: str

    def generate_code(self, scope) -> str:
        code = "_L2:\n"
        code += self.initialization_expression.generate_code(scope)
        code += self.condition_expression.generate_code(scope)
        code += self.statement.generate_code(scope)
        return code


@dataclass
class BreakStatement(Statement):
    pass
