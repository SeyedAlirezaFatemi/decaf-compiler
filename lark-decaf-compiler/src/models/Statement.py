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
        # TODO: Check this.
        for var_decl in self.variable_declarations:
            code += var_decl.generate_code(symbol_table)
        for statement in self.statements:
            code += statement.generate_code(symbol_table)
        # Clean block scope cause we are out of the block
        symbol_table.set_current_scope(statement_block_scope.parent_scope)
        return code, symbol_table


@dataclass
class OptionalExpressionStatement(Statement):
    expression: Optional[Expression] = None


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
    while_number: int
    start_label: str = "UNSPECIFIED"
    end_label: str = "UNSPECIFIED"
    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        code = ""
        symbol_table.enter_loop(self)
        self.while_number = symbol_table.get_current_while_number()
        self.start_label = "for " + str(self.while_number)
        self.end_label = "endfor " + str(self.while_number)
        code += self.start_label + ": \n"
        code += self.condition_expression.generate_code()
        code += "beqz $t1," + self.end_label
        code += self.body_statement.generate_code()
        code += self.update_expression.generate_code()
        code += self.end_label
        symbol_table.exit_loop()
        return code, symbol_table


@dataclass
class ForStatement(Statement):
    initialization_expression: Optional[Expression]
    condition_expression: Expression
    update_expression: Optional[Expression]
    body_statement: Statement
    for_number: int
    start_label: str = "UNSPECIFIED"
    end_label: str = "UNSPECIFIED"

    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        code = ""
        symbol_table.enter_loop(self)
        self.for_number=symbol_table.get_current_for_number()
        self.start_label="for " + str(self.for_number)
        self.end_label="endfor " + str(self.for_number)
        code+=self.initialization_expression.generate_code()
        code+=self.start_label +": \n"
        code+=self.condition_expression.generate_code()
        code+="beqz $t1,"+ self.end_label
        code+=self.body_statement.generate_code()
        code+=self.update_expression.generate_code()
        code+=self.end_label

        symbol_table.exit_loop()
        return code, symbol_table




LoopStatement = Union[WhileStatement, ForStatement]


@dataclass
class BreakStatement(Statement):
    def generate_code(self, symbol_table: SymbolTable) -> Tuple[str, SymbolTable]:
        current_loop_statement = symbol_table.get_current_loop_statement()
        end_label = current_loop_statement.end_label
        return f"j {end_label}", symbol_table
