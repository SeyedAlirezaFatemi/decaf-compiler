from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING, Union

from .Declaration import VariableDeclaration
from .Node import Node

if TYPE_CHECKING:
    from .SymbolTable import SymbolTable
    from .Expression import Expression


@dataclass
class Statement(Node):
    pass


@dataclass
class StatementBlock(Statement):
    variable_declarations: List[VariableDeclaration]
    statements: List[Statement]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        statement_block_scope = symbol_table.enter_new_scope()
        code = []
        for var_decl in self.variable_declarations:
            code += var_decl.generate_code(symbol_table)
        for statement in self.statements:
            code += statement.generate_code(symbol_table)
        # Pop variables in order to correct local offset
        freed_space = symbol_table.pop_variables_till_block(
            symbol_table.get_current_scope(), statement_block_scope
        )
        code.append(f"addiu $sp, $sp, {freed_space} # Freed space")
        # Clean block scope cause we are out of the block
        symbol_table.set_current_scope(statement_block_scope.parent_scope)
        return code


@dataclass
class OptionalExpressionStatement(Statement):
    expression: Optional[Expression] = None


@dataclass
class IfStatement(Statement):
    condition_expression: Expression
    body_statement: Statement
    else_body_statement: Optional[Statement] = None
    if_number: int = 0
    else_number: int = 0
    start_if_label: str = "UNSPECIFIED"
    end_if_label: str = "UNSPECIFIED"
    start_else_label: str = "UNSPECIFIED"
    end_else_label: str = "UNSPECIFIED"

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        if self.else_body_statement is None:
            self.if_number = symbol_table.get_current_if_number()
            self.end_if_label = f"end_if_{self.if_number}"
            code += self.condition_expression.generate_code(symbol_table)
            code.append(f"beqz $t1, {self.end_if_label}")
            code += self.body_statement.generate_code(symbol_table)
            code.append(f"{self.end_if_label}:")

        else:
            self.else_number = symbol_table.get_current_else_number()
            self.start_else_label = f"else_{self.else_number}"
            self.end_else_label = f"end_else_{self.else_number}"
            code += self.condition_expression.generate_code(symbol_table)
            code.append(f"beqz $t1, {self.start_else_label}")
            code += self.body_statement.generate_code(symbol_table)
            code.append(f"jmp {self.end_else_label}")
            code.append(f"{self.start_else_label}:")
            code += self.else_body_statement.generate_code(symbol_table)
            code.append(f"{self.end_else_label}:")

        return code


@dataclass
class ReturnStatement(Statement):
    return_expression: Optional[Expression]


@dataclass
class PrintStatement(Statement):
    args: List[Expression]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        # We assume the output of expressions are saved in $t0
        code = []
        for expression in self.args:
            code += expression.generate_code(symbol_table)
            code.append("subu $sp, $sp, 4\t# decrement sp to make space for print param")
            code.append("sw $t0, 4($sp)\t# copy param value to stack")
            if expression.evaluate_type(symbol_table) == int:
                code.append(f"jal PrintInt")
            elif expression.evaluate_type(symbol_table) == str:
                code.append(f"jal PrintString")
            elif expression.evaluate_type(symbol_table) == bool:
                code.append(f"jal PrintBool")
        return code


@dataclass
class WhileStatement(Statement):
    condition_expression: Expression
    body_statement: Statement
    while_number: int = 0
    start_label: str = "UNSPECIFIED"
    end_label: str = "UNSPECIFIED"

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        symbol_table.enter_loop(self)
        self.while_number = symbol_table.get_current_while_number()
        self.start_label = "while_" + str(self.while_number)
        self.end_label = "end_while_" + str(self.while_number)
        code.append(f"{self.start_label}:")
        code += self.condition_expression.generate_code(symbol_table)
        code.append(f"beqz $t1,{self.end_label}")
        code += self.body_statement.generate_code(symbol_table)
        code.append(f"{self.end_label}:")
        symbol_table.exit_loop()
        return code


@dataclass
class ForStatement(Statement):
    initialization_expression: Optional[Expression]
    condition_expression: Expression
    update_expression: Optional[Expression]
    body_statement: Statement
    for_number: int = 0
    start_label: str = "UNSPECIFIED"
    end_label: str = "UNSPECIFIED"

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        symbol_table.enter_loop(self)
        self.for_number = symbol_table.get_current_for_number()
        self.start_label = "for_" + str(self.for_number)
        self.end_label = "end_for_" + str(self.for_number)

        if self.initialization_expression is not None:
            code += self.initialization_expression.generate_code(symbol_table)
        code.append(f"{self.start_label}:")
        code += self.condition_expression.generate_code(symbol_table)
        code.append(f"beqz $t1,{self.end_label}")
        code += self.body_statement.generate_code(symbol_table)
        if self.update_expression is not None:
            code += self.update_expression.generate_code(symbol_table)
        code.append(f"{self.end_label}:")

        symbol_table.exit_loop()
        return code


LoopStatement = Union[WhileStatement, ForStatement]


@dataclass
class BreakStatement(Statement):
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        current_loop_statement = symbol_table.get_current_loop_statement()
        end_label = current_loop_statement.end_label
        return [f"j {end_label}"]
