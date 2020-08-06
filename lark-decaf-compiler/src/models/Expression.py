from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List, Union, Tuple

from .Declaration import ClassDeclaration, FunctionDeclaration, VariableDeclaration
from .Identifier import Identifier
from .Node import Node
from .Type import Type, PrimitiveTypes, NamedType, ArrayType
from ..utils import (
    calc_variable_size,
    pop_to_temp,
    push_to_stack,
    pop_double_to_femp,
    push_double_to_stack,
    ARRAY_LENGTH_SIZE,
)

if TYPE_CHECKING:
    from .SymbolTable import SymbolTable
    from typing import TYPE_CHECKING


class Operator(Enum):
    MINUS = "-"
    ADDITION = "+"
    NOT = "!"
    DIVISION = "/"
    MULTIPLICATION = "*"
    MODULO = "%"
    LTE = "<="
    GTE = ">="
    LT = "<"
    GT = ">"
    EQUALS = "=="
    NOT_EQUALS = "!="
    AND = "&&"
    OR = "||"


"""
When we generate code for expressions, we push their result to stack.
So if you have multiple expressions, first call generate_code on all of them, and then
    start popping values from stack to access their results.
"""


@dataclass
class Expression(Node):
    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        pass


@dataclass
class BinaryExpression(Expression):
    operator: Operator
    left_expression: Expression
    right_expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        if self.operator in {
            Operator.AND,
            Operator.OR,
            Operator.LT,
            Operator.LTE,
            Operator.GT,
            Operator.GTE,
            Operator.EQUALS,
            Operator.NOT_EQUALS,
        }:
            return Type(PrimitiveTypes.BOOL.value)
        else:
            return self.left_expression.evaluate_type(symbol_table)

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        left_operand_type = self.left_expression.evaluate_type(symbol_table)
        right_operand_type = self.right_expression.evaluate_type(symbol_table)
        assert left_operand_type == right_operand_type
        operand_type = left_operand_type
        code = []
        code += self.left_expression.generate_code(symbol_table)
        code += self.right_expression.generate_code(symbol_table)
        if self.operator == Operator.ADDITION:
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("addu $t2,$t1,$t0")
                code += push_to_stack(2)
            else:
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("add.d $f4, $f2, $f0")
                code += push_double_to_stack(4)
        elif self.operator == Operator.MINUS:
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("sub $t2,$t1,$t0")
                code += push_to_stack(2)
            else:
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("sub.d $f4, $f2, $f0")
                code += push_double_to_stack(4)
        elif self.operator == Operator.MULTIPLICATION:
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("mul $t2,$t1,$t0")
                code += push_to_stack(2)
            else:
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("mul.d $f4, $f2, $f0")
                code += push_double_to_stack(4)
        elif self.operator == Operator.DIVISION:
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("div $t2,$t1,$t0")
                code += push_to_stack(2)
            else:
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("div.d $f4, $f2, $f0")
                code += push_double_to_stack(4)
        elif self.operator == Operator.MODULO:
            code += pop_to_temp(0)
            code += pop_to_temp(1)
            code.append("div $t2,$t1,$t0")
            code.append("mfhi $t2")
            code += push_to_stack(2)
        elif self.operator == Operator.LTE:
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("sle $t2,$t1,$t0")
                code += push_to_stack(2)
            else:
                counter = symbol_table.get_label()
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("c.le.d $f2,$f0")
                code.append(f"bc1f __double_le__{counter}")
                code.append("li $t0, 1")
                code.append(f"__double_le__{counter}:")
                code += push_to_stack(0)
        elif self.operator == Operator.LT:
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("slt $t2,$t1,$t0")
                code += push_to_stack(2)
            else:
                counter = symbol_table.get_label()
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("c.lt.d $f2,$f0")
                code.append(f"bc1f __double_le__{counter}")
                code.append("li $t0, 1")
                code.append(f"__double_le__{counter}:")
                code += push_to_stack(0)
        elif self.operator == Operator.GTE:
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("sge $t2,$t1,$t0")
                code += push_to_stack(2)
            else:
                counter = symbol_table.get_label()
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("c.lt.d $f2,$f0")
                code.append(f"bc1t __double_le__{counter}")
                code.append("li $t0, 1")
                code.append(f"__double_le__{counter}:")
                code += push_to_stack(0)
        elif self.operator == Operator.GT:
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("sgt $t2,$t1,$t0")
                code += push_to_stack(2)
            else:
                counter = symbol_table.get_label()
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("c.le.d $f2,$f0")
                code.append(f"bc1t __double_le__{counter}")
                code.append("li $t0, 1")
                code.append(f"__double_le__{counter}:")
                code += push_to_stack(0)
        elif self.operator == Operator.AND:
            code += pop_to_temp(0)
            code += pop_to_temp(1)
            code.append("and $t2,$t1,$t0")
            code += push_to_stack(2)
        elif self.operator == Operator.OR:
            code += pop_to_temp(0)
            code += pop_to_temp(1)
            code.append("or $t2,$t1,$t0")
            code += push_to_stack(2)
        elif self.operator == Operator.EQUALS:  # TODO: String
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("seq $t2,$t1,$t0")
                code += push_to_stack(2)
            elif operand_type == "double":
                counter = symbol_table.get_label()
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("c.eq.d $f2,$f0")
                code.append(f"bc1f __double_le__{counter}")
                code.append("li $t0, 1")
                code.append(f"__double_le__{counter}:")
                code += push_to_stack(0)
            # else:
        elif self.operator == Operator.NOT_EQUALS:  # TODO: String
            if operand_type == "int":
                code += pop_to_temp(0)
                code += pop_to_temp(1)
                code.append("sne $t2,$t1,$t0")
                code += push_to_stack(2)
            elif operand_type == "double":
                counter = symbol_table.get_label()
                code += pop_double_to_femp(0)
                code += pop_double_to_femp(2)
                code.append("c.eq.d $f2,$f0")
                code.append(f"bc1t __double_le__{counter}")
                code.append("li $t0, 1")
                code.append(f"__double_le__{counter}:")
                code += push_to_stack(0)
            # else:

        return code


@dataclass
class UnaryExpression(Expression):
    operator: Operator
    expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        if self.operator == Operator.MINUS:
            return self.expression.evaluate_type(symbol_table)
        elif self.operator == Operator.NOT:
            return Type(PrimitiveTypes.BOOL.value)

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = self.expression.generate_code(symbol_table)
        operand_type = self.expression.evaluate_type(symbol_table)
        if self.operator == Operator.MINUS:
            if operand_type == "int":
                code += pop_to_temp(0)
                code.append("addi $t1, $zero, -1")
                code.append("mul $t2,$t0,$t1")
                code += push_to_stack(2)
            else:
                code += pop_double_to_femp(0)
                code.append("addi $f2, $zero, -1")
                code.append("mul.d $f4, $f2, $f0")
                code += push_double_to_stack(4)
        elif self.operator == Operator.NOT:
            code += pop_to_temp(0)
            code.append("nor $t0, $t0, $t0")
            code += push_to_stack(0)
        return code


@dataclass
class ThisExpression(Expression):
    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        class_decl = symbol_table.get_current_scope().find_which_class_we_are_in()
        return NamedType(class_decl.identifier)


@dataclass
class ReadInteger(Expression):
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = [f"\tjal _ReadInteger"]
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return Type(PrimitiveTypes.INT.value)


@dataclass
class ReadLine(Expression):
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = [f"\tjal _ReadLine"]
        code += [
            f"\tsubu $sp,$sp,4\t# make space for string pointer",
            f"\tsw $v0,4($sp)\t#copy string pointer to stack",
        ]
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return Type(PrimitiveTypes.STRING.value)


@dataclass
class LValue(Expression):
    def calculate_address(self, symbol_table: SymbolTable) -> Tuple[List[str], str]:
        pass


OFFSET_TO_FIRST_LOCAL = -8
OFFSET_TO_FIRST_PARAM = 4
OFFSET_TO_FIRST_GLOBAL = 0


@dataclass
class IdentifierLValue(LValue):
    identifier: Identifier

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = [f"\t# Code for identifier {self.identifier.name}"]
        _, address = self.calculate_address(symbol_table)
        code.append(f"\tlw $t0, {address}\t# load value from {address} to $t0")
        code += push_to_stack(0)
        code.append(f"\t# End of code for identifier {self.identifier.name}")
        return code

    def calculate_address(self, symbol_table: SymbolTable) -> Tuple[List[str], str]:
        """
        In a MIPS stack frame, first local is at fp-8, subsequent locals are at fp-12, fp-16, and so on.
        The first param is at fp+4, subsequent ones as fp+8, fp+12, etc. (Because methods have secret
        "this" passed in first param slot at fp+4, all normal params are shifted up by 4.)
        """
        code = []
        decl = self.identifier.find_declaration(symbol_table)
        assert isinstance(decl, VariableDeclaration)
        if decl.is_class_member:
            # TODO: use this to calc address. use vtable.
            decl.class_member_offset
        elif decl.is_function_parameter:
            return (
                code,
                f"{OFFSET_TO_FIRST_PARAM + decl.function_parameter_offset}($fp)",
            )
        elif decl.is_global:
            return code, f"{OFFSET_TO_FIRST_GLOBAL - decl.global_offset}($gp)"
        else:
            return code, f"{OFFSET_TO_FIRST_LOCAL - decl.local_offset}($fp)"

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.identifier.evaluate_type(symbol_table)


@dataclass
class MemberAccessLValue(LValue):
    expression: Expression
    identifier: Identifier

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        class_type = self.expression.evaluate_type(symbol_table)
        assert isinstance(class_type, NamedType)
        class_decl = symbol_table.get_global_scope().lookup(class_type.name)
        assert isinstance(class_decl, ClassDeclaration)
        return class_decl.find_variable_declaration(self.identifier).variable_type


@dataclass
class ArrayAccessLValue(LValue):
    array_expression: Expression
    index_expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        array_type = self.array_expression.evaluate_type(symbol_table)
        assert isinstance(array_type, ArrayType)
        return array_type.element_type

    def calculate_address(self, symbol_table: SymbolTable) -> Tuple[List[str], str]:
        array_type = self.array_expression.evaluate_type(symbol_table)
        assert isinstance(array_type, ArrayType)
        array_element_size = calc_variable_size(array_type.element_type)
        code = ["\t# Code for array access"]
        code += self.array_expression.generate_code(
            symbol_table
        )  # pushes array address
        code += self.index_expression.generate_code(symbol_table)  # pushes index
        code += pop_to_temp(1)  # index at $t0
        code += pop_to_temp(0)  # array address at $t0
        code.append(f"\tsll $t1,$t1,{int(math.sqrt(array_element_size))}")
        code.append(
            f"\taddi $t1, $t1, {ARRAY_LENGTH_SIZE} # extra {ARRAY_LENGTH_SIZE} bytes for length of array"
        )
        code.append("\taddu $t2,$t1,$t0\t# address of element is now in $t2")
        code.append("\t# End of code for array access")
        return code, "0($t2)"

    def generate_code(self, symbol_table: SymbolTable):
        array_type = self.array_expression.evaluate_type(symbol_table)
        assert isinstance(array_type, ArrayType)
        code = ["\t# Code for array access + use"]
        access_code, access_address = self.calculate_address(symbol_table)
        code += access_code
        if array_type.element_type == "int":
            code.append(f"\tlw $t0, {access_address}")
            code += push_to_stack(0)
        elif array_type.element_type == "double":
            code.append(f"\tl.d $f0, {access_address}")
            code += push_double_to_stack(0)
        code.append("\t# End of code for array access + use")
        return code


@dataclass
class Assignment(Expression):
    l_value: LValue
    expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.expression.evaluate_type(symbol_table)

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = self.expression.generate_code(symbol_table)
        # We do not generate_code for l_value. We only need address.
        if self.expression.evaluate_type(symbol_table) == "double":
            l_value_code, l_value_address = self.l_value.calculate_address(symbol_table)
            code += l_value_code
            code += pop_double_to_femp(0)  # expression result
            code.append(f"\ts.d $f0, {l_value_address}\t# assignment")
        else:
            l_value_code, l_value_address = self.l_value.calculate_address(symbol_table)
            code += l_value_code
            code += pop_to_temp(0)  # expression result
            code.append(f"\tsw $t0, {l_value_address}\t# assignment")
        return code


@dataclass
class Call(Expression):
    pass


@dataclass
class FunctionCall(Call):
    function_identifier: Identifier
    actual_parameters: List[Expression]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        function_decl = self._find_function_decl()
        function_label = function_decl.label
        # TODO: call function

        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self._find_function_decl().return_type

    def _find_function_decl(self) -> FunctionDeclaration:
        function_decl = self.function_identifier.declaration
        assert isinstance(function_decl, FunctionDeclaration)
        return function_decl


@dataclass
class MethodCall(Call):
    class_expression: Expression
    method_identifier: Identifier
    actual_parameters: List[Expression]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        method_decl = self._find_method_decl()
        method_label = method_decl.label
        # TODO: call method
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self._find_method_decl().return_type

    def _find_method_decl(self) -> FunctionDeclaration:
        method_decl = self.method_identifier.declaration
        assert isinstance(method_decl, FunctionDeclaration)
        return method_decl


@dataclass
class InitiateClass(Expression):
    class_identifier: Identifier

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return NamedType(self.class_identifier)


@dataclass
class InitiateArray(Expression):
    length_expression: Expression
    element_type: Type

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        type_size = calc_variable_size(self.element_type)
        code = []
        code += self.length_expression.generate_code(symbol_table)
        code += pop_to_temp(0)  # now array size is in t0
        code += [
            "\tmove $a0, $t0\t# move array length to $a0",
            f"\tsll $a0, $a0, {int(math.sqrt(type_size))}\t# size of array",
            f"\taddi $a0, $a0, {ARRAY_LENGTH_SIZE} # extra {ARRAY_LENGTH_SIZE} bytes for length of array",
            "\tli $v0, 9\t#rsbrk",
            "\tsyscall",
            "\tsw $t0 0($v0)\t# copy array length to the start of array",
            # "\taddi $v0, $v0, 4\t# move array pointer after length",
            "\tsub $sp, $sp, 4\t# make space for array pointer",
            "\tsw $v0, 4($sp)\t# save array pointer to stack",
        ]
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return ArrayType(self.element_type)


@dataclass
class Constant(Expression):
    constant_type: Type
    value: Union[bool, str, int, float]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        size = calc_variable_size(self.constant_type)
        code = [
            f"\t# Code for constant {self.value}",
            f"\tsubu $sp, $sp, {size}\t# decrement sp to make space for constant {self.value}",
        ]
        if self.constant_type == PrimitiveTypes.DOUBLE:
            code += [
                f"\tli.d $f12, {self.value}\t# load constant value to $f12",
                f"\ts.d $f12, {size}($sp)\t# load constant value from $f12 to {size}($sp)",
            ]
        elif self.constant_type == PrimitiveTypes.BOOL:
            code += [
                f"\tli $t0, {1 if self.value == 'true' else 0}\t# load constant value to $t0",
                f"\tsw $t0, {size}($sp)\t# load constant value from $t0 to {size}($sp)",
            ]
        else:
            code += [
                f"\tli $t0, {self.value}\t# load constant value to $t0",
                f"\tsw $t0, {size}($sp)\t# load constant value from $to to {size}($sp)",
            ]
        code.append(f"\t# End of code for constant {self.value}")
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.constant_type
