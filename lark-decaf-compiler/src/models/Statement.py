from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING, Tuple, Union

from .Node import Node

if TYPE_CHECKING:
    from .SymbolTable import SymbolTable
    from .Declaration import VariableDeclaration
    from .Expression import Expression


@dataclass
class Statement(Node):
    pass


@dataclass
class StatementBlock(Statement):
    variable_declarations: List[VariableDeclaration]
    statements: List[Statement]

    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        statement_block_scope = symbol_table.enter_new_scope()
        code = ""
        for var_decl in self.variable_declarations:
            new_code, symbol_table = var_decl.generate_code(symbol_table)
            code += new_code
        for statement in self.statements:
            new_code, symbol_table = statement.generate_code(symbol_table)
            code += new_code
        # Clean block scope cause we are out of the block
        symbol_table.set_current_scope(statement_block_scope.parent_scope)
        return code, symbol_table


@dataclass
class OptionalExpressionStatement(Statement):
    expression: Optional[Expression] = None

    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        if self.expression is None:
            return "", symbol_table
        return self.expression.generate_code(symbol_table)


@dataclass
class IfStatement(Statement):
    condition_expression: Expression
    body_statement: Statement
    else_body_statement: Optional[Statement] = None


@dataclass
class ReturnStatement(Statement):
    return_expression: Optional[Expression]


@dataclass
class PrintStatement(Statement):
    args: List[Expression]

    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        # TODO: generate code for each expression then based on output type call the
        # print function in standard_library_functions.py
        pass


@dataclass
class WhileStatement(Statement):
    condition_expression: Expression
    body_statement: Statement
    end_label: str = "UNSPECIFIED"

    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        code = ""
        symbol_table.enter_loop(self)
        # TODO: code generation
        symbol_table.exit_loop()
        return code, symbol_table


@dataclass
class ForStatement(Statement):
    initialization_expression: Optional[Expression]
    condition_expression: Expression
    update_expression: Optional[Expression]
    body_statement: Statement
    end_label: str = "UNSPECIFIED"

    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        code = ""
        symbol_table.enter_loop(self)
        # TODO: code generation
        symbol_table.exit_loop()
        return code, symbol_table


LoopStatement = Union[WhileStatement, ForStatement]


@dataclass
class BreakStatement(Statement):
    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        current_loop_statement = symbol_table.get_current_loop_statement()
        end_label = current_loop_statement.end_label
        return f"j {end_label}", symbol_table
