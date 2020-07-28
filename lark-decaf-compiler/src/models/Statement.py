from typing import List, Optional

from .Declaration import VariableDeclaration
from .Expression import Expression
from .Node import Node


class Statement(Node):
    pass


class StatementBlock(Statement):
    variable_declarations: List[VariableDeclaration]
    statements: List[Statement]


class IfStatement(Statement):
    condition_expression: Expression
    body_statement: Statement
    else_body_statement: Statement


class WhileStatement(Statement):
    condition_expression: Expression
    body_statement: Statement
    end_label: str


class ReturnStatement(Statement):
    return_expression: Optional[Expression]


class PrintStatement(Statement):
    args: List[Expression]


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


class BreakStatement(Statement):
    pass
