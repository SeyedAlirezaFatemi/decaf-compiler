from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List, Union, Tuple, Optional

from .Declaration import ClassDeclaration, FunctionDeclaration, VariableDeclaration
from .Identifier import Identifier
from .Node import Node
from .Type import Type, PrimitiveTypes, NamedType, ArrayType
from ..standard_library_functions import STANDARD_LIBRARY_FUNCTIONS
from ..utils import (
    calc_variable_size,
    pop_to_temp,
    push_to_stack,
    pop_double_to_femp,
    push_double_to_stack,
    ARRAY_LENGTH_SIZE,
    THIS_ADDRESS,
    DOUBLE_RETURN_REGISTER_NUMBER,
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
Don't forget to pop expressions results after evaluating them.
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
                code.append("add $t2,$t1,$t0")
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
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = [
            "\t# Code for 'this' expression",
            f"\tsubu $sp,$sp,4\t# Make space for 'this' pointer",
            f"\tlw $t0,{THIS_ADDRESS}\t# Copy 'this' pointer pointer to $t0",
            f"\tsw $t0,4($sp)\t# Copy 'this' pointer pointer to stack",
            "\t# End of code for 'this' expression",
        ]
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        class_decl = symbol_table.get_current_scope().find_which_class_we_are_in()
        return NamedType(class_decl.identifier)


@dataclass
class ReadInteger(Expression):
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = [f"\tjal _ReadInteger"]
        code += [
            f"\tsubu $sp,$sp,4\t# Make space for Integer.",
            f"\tsw $v0,4($sp)\t# Copy Integer to stack.",
        ]
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return Type(PrimitiveTypes.INT.value)


@dataclass
class ReadLine(Expression):
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = [f"\tjal _ReadLine"]
        code += [
            f"\tsubu $sp,$sp,4\t# Make space for string pointer.",
            f"\tsw $v0,4($sp)\t# Copy string pointer to stack.",
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
        address_calculation_code, address = self.calculate_address(symbol_table)
        code += address_calculation_code
        if self.evaluate_type(symbol_table) == PrimitiveTypes.DOUBLE:
            code.append(f"\tl.d $f0, {address}\t# Load value from {address} to $f0")
            code += push_double_to_stack(0)
        else:
            code.append(f"\tlw $t0, {address}\t# Load value from {address} to $t0")
            code += push_to_stack(0)
        code.append(
            f"\t# End of code for identifier {self.identifier.name}. Identifier value is on top of stack now."
        )
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
        # To load and save double, pointer must point to the end of double.
        double_offset = 0
        if decl.variable_type == PrimitiveTypes.DOUBLE:
            double_offset = 8
        if decl.is_class_member:
            # Class members only accessible in class methods. They're protected.
            return calculate_member_address(decl.class_member_offset - double_offset)
        elif decl.is_function_parameter:
            return (
                code,
                f"{OFFSET_TO_FIRST_PARAM + decl.function_parameter_offset + calc_variable_size(decl.variable_type) - double_offset}($fp)",
            )
        elif decl.is_global:
            return (
                code,
                f"{OFFSET_TO_FIRST_GLOBAL - decl.global_offset - double_offset}($gp)",
            )
        else:
            return (
                code,
                f"{OFFSET_TO_FIRST_LOCAL - decl.local_offset - double_offset}($fp)",
            )

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.identifier.evaluate_type(symbol_table)


def calculate_member_address(member_offset: int) -> Tuple[List[str], str]:
    code = [
        "\t# Code for class member address calculation:",
        f"\tlw $t0, {THIS_ADDRESS}\t# Load 'this' address to $t0.",
        f"\taddi $t0, $t0, {member_offset}\t# Extra {member_offset} bytes for member offset.",
        "\tmove $t1, $t0\t# Copy member address to $t1.",
        "\t# End of code for class member address calculation. Member address is in $t1 now.",
    ]
    return code, "0($t1)"


@dataclass
class MemberAccessLValue(LValue):
    expression: Expression
    identifier: Identifier

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        # Only way to access members. We cant use them outside of the object.
        assert isinstance(self.expression, ThisExpression)
        var_decl = self.find_declaration(symbol_table)
        code = ["\t# Code for class member access:"]
        address_calculation_code, address = calculate_member_address(
            var_decl.class_member_offset
        )
        code += address_calculation_code
        if var_decl.variable_type == PrimitiveTypes.DOUBLE:
            code.append(f"\tl.d $f0, {address}\t# Load value from {address} to $f0.")
            code += push_double_to_stack(0)
        else:
            code.append(f"\tlw $t0, {address}\t# Load value from {address} to $t0.")
            code += push_to_stack(0)
        code.append(
            "\t# End of code for class member access. Member value is on top of stack now."
        )
        return code

    def calculate_address(self, symbol_table: SymbolTable) -> Tuple[List[str], str]:
        var_decl = self.find_declaration(symbol_table)
        return calculate_member_address(var_decl.class_member_offset)

    def find_declaration(self, symbol_table: SymbolTable) -> VariableDeclaration:
        var_decl = symbol_table.get_current_scope().lookup_in_class_members(
            symbol_table, self.identifier
        )
        assert isinstance(var_decl, VariableDeclaration)
        return var_decl

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        # Based on language description, object members are protected.
        assert isinstance(self.expression, ThisExpression)
        class_type = self.expression.evaluate_type(symbol_table)
        assert isinstance(class_type, NamedType)
        class_decl = symbol_table.get_global_scope().lookup(class_type.name)
        assert isinstance(class_decl, ClassDeclaration)
        return class_decl.find_variable_declaration(
            symbol_table, self.identifier
        ).variable_type


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
            f"\taddi $t1, $t1, {ARRAY_LENGTH_SIZE}\t# Extra {ARRAY_LENGTH_SIZE} bytes for length of array"
        )
        code.append("\taddu $t2,$t1,$t0\t# Address of element is now in $t2")
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
            code += pop_double_to_femp(0)  # Expression result
            code.append(f"\ts.d $f0, {l_value_address}\t# assignment")
            # Push expression result to stack
            code += push_double_to_stack(0)
        else:
            l_value_code, l_value_address = self.l_value.calculate_address(symbol_table)
            code += l_value_code
            code += pop_to_temp(0)  # expression result
            code.append(f"\tsw $t0, {l_value_address}\t# assignment")
            # Push expression result to stack
            code += push_to_stack(0)
        return code


@dataclass
class Call(Expression):
    pass


@dataclass
class FunctionCall(Call):
    function_identifier: Identifier
    actual_parameters: List[Expression]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        function_decl = self._find_function_decl(symbol_table)
        if function_decl.is_method:
            # For when we call object method without this.
            return generate_call(
                symbol_table, function_decl, self.actual_parameters, is_method=True
            )
        return generate_call(
            symbol_table, function_decl, self.actual_parameters, is_method=False
        )

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self._find_function_decl(symbol_table).return_type

    def _find_function_decl(self, symbol_table: SymbolTable) -> FunctionDeclaration:
        function_decl = self.function_identifier.find_declaration(symbol_table)
        assert isinstance(function_decl, FunctionDeclaration)
        return function_decl


def generate_call(
    symbol_table: SymbolTable,
    function_decl: FunctionDeclaration,
    actual_parameters: List[Expression],
    is_method: bool = False,
    class_expression: Optional[Expression] = None,
):
    code = [f"\t# Code for {'method' if is_method else 'function'} call."]
    return_type = function_decl.return_type
    return_size = calc_variable_size(return_type)
    function_label = function_decl.label
    parameter_bytes = 0
    for parameter in actual_parameters:
        parameter_bytes += calc_variable_size(parameter.evaluate_type(symbol_table))
    for parameter in reversed(actual_parameters):
        code += parameter.generate_code(symbol_table)
    if not is_method:
        if function_decl not in STANDARD_LIBRARY_FUNCTIONS:  # No this for standards.
            code += [f"\tsubu $sp, $sp, 4\t# Make space for 'this'. It won't be used."]
    elif is_method and class_expression is not None:
        code += class_expression.generate_code(symbol_table)
    elif is_method:
        # When we call object method without this. We add it implicitly.
        code += ThisExpression().generate_code(symbol_table)
    code += [f"\tjal {function_label}"]
    if function_decl not in STANDARD_LIBRARY_FUNCTIONS:  # No this for standards.
        code.append(
            f"\taddiu $sp, $sp, {parameter_bytes + 4}\t# Cleanse stack of function parameters."
        )
    else:
        # Did not push this for standards.
        code.append(
            f"\taddiu $sp, $sp, {parameter_bytes}\t# Cleanse stack of function parameters."
        )
    # Return value is in $v0 for non double return types. For double it's in $f0.
    if return_type == PrimitiveTypes.DOUBLE:
        code += push_double_to_stack(DOUBLE_RETURN_REGISTER_NUMBER)
    else:
        # Warning: We do this even for void functions.
        code += [
            f"\tsubu $sp, $sp, {return_size}\t# Make space for function return value.",
            f"\tsw $v0, {return_size}($sp)\t# Copy return value to stack.",
        ]
    code.append(f"\t# End of Code for {'method' if is_method else 'function'} call.")
    return code


@dataclass
class MethodCall(Call):
    class_expression: Expression
    method_identifier: Identifier
    actual_parameters: List[Expression]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        left_type = self.class_expression.evaluate_type(symbol_table)
        if left_type.is_array():
            assert self.method_identifier.name == "length"
            array_expression = self.class_expression
            code += array_expression.generate_code(
                symbol_table
            )  # array pointer in stack now
            code += pop_to_temp(0)  # array pointer in stack now
            code += ["\tlw $t1, 0($t0)\t# Move array length to $t1"]
            code += push_to_stack(1)
            return code
        method_decl = self._find_method_decl(symbol_table)
        call_code = generate_call(
            symbol_table,
            method_decl,
            self.actual_parameters,
            is_method=True,
            class_expression=self.class_expression,
        )
        code += call_code
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        left_type = self.class_expression.evaluate_type(symbol_table)
        if left_type.is_array():
            assert self.method_identifier.name == "length"
            return Type(PrimitiveTypes.INT.value)
        return self._find_method_decl(symbol_table).return_type

    def _find_class_decl(self, symbol_table: SymbolTable) -> ClassDeclaration:
        class_type = self.class_expression.evaluate_type(symbol_table)
        assert isinstance(class_type, NamedType)
        class_decl = symbol_table.get_global_scope().lookup(class_type.name)
        assert isinstance(class_decl, ClassDeclaration)
        return class_decl

    def _find_method_decl(self, symbol_table: SymbolTable) -> FunctionDeclaration:
        class_decl = self._find_class_decl(symbol_table)
        method_decl = class_decl.find_method_declaration(
            symbol_table, self.method_identifier
        )
        assert isinstance(method_decl, FunctionDeclaration)
        return method_decl


@dataclass
class InitiateClass(Expression):
    class_identifier: Identifier

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        class_decl = self.class_identifier.find_declaration(symbol_table)
        assert isinstance(class_decl, ClassDeclaration)
        object_size = class_decl.calculate_size(symbol_table)
        code = [f"\t# Code for object of type {self.class_identifier.name} initiation:"]
        code += [
            f"\tli $a0, {object_size}\t# Load object size to $a0.",
            "\tli $v0, 9\t# rsbrk.",
            "\tsyscall\t# Object pointer is now in $v0.",
            "\tsub $sp, $sp, 4\t# Make space for object pointer.",
            "\tsw $v0, 4($sp)\t# Save object pointer to stack.",
            f"\t# End of code for object of type {self.class_identifier.name} initiation. Object pointer is now on top of stack.",
        ]
        return code

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
            "\tmove $a0, $t0\t# Move array length to $a0",
            f"\tsll $a0, $a0, {int(math.sqrt(type_size))}\t# Size of array",
            f"\taddi $a0, $a0, {ARRAY_LENGTH_SIZE}\t# Extra {ARRAY_LENGTH_SIZE} bytes for length of array",
            "\tli $v0, 9\t# rsbrk",
            "\tsyscall",
            "\tsw $t0 0($v0)\t# Copy array length to the start of array",
            # "\taddi $v0, $v0, 4\t# move array pointer after length",
            "\tsub $sp, $sp, 4\t# Make space for array pointer",
            "\tsw $v0, 4($sp)\t# Save array pointer to stack",
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
            self.value = self.value.lower()
            if self.value[-1] == ".":
                self.value += "0"
            if ".e" in self.value:
                index = self.value.find(".e") + 1
                self.value = self.value[:index] + "0" + self.value[index:]
            code += [
                f"\tli.d $f0, {self.value}\t# load constant value to $f12",
                f"\ts.d $f0, 0($sp)\t# load constant value from $f12 to 0($sp)",
            ]
        elif self.constant_type == PrimitiveTypes.BOOL:
            code += [
                f"\tli $t0, {1 if self.value == 'true' else 0}\t# load constant value to $t0",
                f"\tsw $t0, {size}($sp)\t# load constant value from $t0 to {size}($sp)",
            ]
        elif self.constant_type == PrimitiveTypes.STRING:
            name = f"str_{symbol_table.get_string_cost_count()}"
            code += [
                "\t.data",
                f"{name}:",
                f"\t.asciiz {self.value}",
                ".text",
                f"\tla $t0, {name}\t# Load address",
                f"\tsw $t0, {size}($sp)\t# Load address from $t0 to {size}($sp)",
            ]
        elif self.constant_type == PrimitiveTypes.NULL:
            # Do nothing. Right?
            code += []
        else:
            code += [
                f"\tli $t0, {self.value}\t# load constant value to $t0",
                f"\tsw $t0, {size}($sp)\t# load constant value from $to to {size}($sp)",
            ]
        code.append(f"\t# End of code for constant {self.value}")
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.constant_type
