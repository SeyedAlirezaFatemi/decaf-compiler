from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List, Union

from .Declaration import ClassDeclaration, FunctionDeclaration, VariableDeclaration
from .Identifier import Identifier
from .Node import Node
from .Type import Type, PrimitiveTypes, NamedType, ArrayType

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
        return self.left_expression.evaluate_type(symbol_table)

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        code += self.left_expression.generate_code(symbol_table)
        code += self.right_expression.generate_code(symbol_table)
        if self.operator == Operator.ADDITION:
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("addu $t2,$t0,$t1")
                code += spush(2)
            else:
                code += spop_double(0)
                code += spop_double(2)
                code.append("add.d $f4, $f2, $f0")
                code += spush_double(4)
        elif self.operator == Operator.MINUS:
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("sub $t2,$t0,$t1")
                code += spush(2)
            else:
                code += spop_double(0)
                code += spop_double(2)
                code.append("sub.d $f4, $f2, $f0")
                code += spush_double(4)
        elif self.operator == Operator.MULTIPLICATION:
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("mul $t2,$t0,$t1")
                code += spush(2)
            else:
                code += spop_double(0)
                code += spop_double(2)
                code.append("mul.d $f4, $f2, $f0")
                code += spush_double(4)
        elif self.operator == Operator.DIVISION:
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("div $t2,$t0,$t1")
                code += spush(2)
            else:
                code += spop_double(0)
                code += spop_double(2)
                code.append("div.d $f4, $f2, $f0")
                code += spush_double(4)
        elif self.operator == Operator.MODULO:
            code += spop(0)
            code += spop(1)
            code.append("div $t2,$t0,$t1")
            code.append("mfhi $t2")
            code += spush(2)
        elif self.operator == Operator.LTE:  # TODO: double
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("sle $t2,$t1,$t0")
                code += spush(2)
            # else:
            #     code += spop_double(0)
            #     code += spop_double(2)
            #     code.append()
            #     code += spush_double(4)
        elif self.operator == Operator.LT:  # TODO: double
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("slt $t2,$t1,$t0")
                code += spush(2)
            # else:
            #     code += spop_double(0)
            #     code += spop_double(2)
            #     code.append()
            #     code += spush_double(4)
        elif self.operator == Operator.GTE:  # TODO: double
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("sge $t2,$t1,$t0")
                code += spush(2)
            # else:
            #     code += spop_double(0)
            #     code += spop_double(2)
            #     code.append()
            #     code += spush_double(4)
        elif self.operator == Operator.GT:  # TODO: double
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("sgt $t2,$t1,$t0")
                code += spush(2)
            # else:
            #     code += spop_double(0)
            #     code += spop_double(2)
            #     code.append()
            #     code += spush_double(4)
        elif self.operator == Operator.AND:
            code += spop(0)
            code += spop(1)
            code.append("and $t2,$t1,$t0")
            code += spush(2)
        elif self.operator == Operator.OR:
            code += spop(0)
            code += spop(1)
            code.append("or $t2,$t1,$t0")
            code += spush(2)
        elif self.operator == Operator.EQUALS:  # TODO: String and Double
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("seq $t2,$t1,$t0")
                code += spush(2)
            # elif self.evaluate_type(symbol_table) == 'double':
            #     code += spop_double(0)
            #     code += spop_double(2)
            #     code.append()
            #     code += spush_double(4)
            # else:
        elif self.operator == Operator.EQUALS:  # TODO: String and Double
            if self.evaluate_type(symbol_table) == "int":
                code += spop(0)
                code += spop(1)
                code.append("sne $t2,$t1,$t0")
                code += spush(2)
            # elif self.evaluate_type(symbol_table) == 'double':
            #     code += spop_double(0)
            #     code += spop_double(2)
            #     code.append()
            #     code += spush_double(4)
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


@dataclass
class ThisExpression(Expression):
    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        class_decl = symbol_table.get_current_scope().find_which_class_we_are_in()
        return NamedType(class_decl.identifier)


@dataclass
class ReadInteger(Expression):
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        # TODO: call the _ReadInteger function in standard_library_functions.py
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return Type(PrimitiveTypes.INT.value)


@dataclass
class ReadLine(Expression):
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        # TODO: call the _ReadLine function in standard_library_functions.py
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return Type(PrimitiveTypes.STRING.value)


@dataclass
class LValue(Expression):
    def calculate_address(self, symbol_table: SymbolTable):
        pass


OFFSET_TO_FIRST_LOCAL = -8
OFFSET_TO_FIRST_PARAM = 4
OFFSET_TO_FIRST_GLOBAL = 0


@dataclass
class IdentifierLValue(LValue):
    identifier: Identifier

    def calculate_address(self, symbol_table: SymbolTable):
        """
        In a MIPS stack frame, first local is at fp-8, subsequent locals are at fp-12, fp-16, and so on.
        The first param is at fp+4, subsequent ones as fp+8, fp+12, etc. (Because methods have secret
        "this" passed in first param slot at fp+4, all normal params are shifted up by 4.)
        """
        decl = self.identifier.declaration
        assert isinstance(decl, VariableDeclaration)
        if decl.is_class_member:
            # TODO: use this to calc address. use vtable.
            decl.class_member_offset
        elif decl.is_function_parameter:
            return f"{OFFSET_TO_FIRST_PARAM + decl.function_parameter_offset}($fp)"
        elif decl.is_global:
            return f"{OFFSET_TO_FIRST_GLOBAL - decl.global_offset}($gp)"
        else:
            return f"{OFFSET_TO_FIRST_LOCAL - decl.local_offset}($fp)"

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.identifier.evaluate_type(symbol_table)

    def generate_code(self, symbol_table: SymbolTable):
        # TODO:
        pass


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
        return array_type.elementType


@dataclass
class Assignment(Expression):
    l_value: LValue
    expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.expression.evaluate_type(symbol_table)


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

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return ArrayType(self.element_type)


@dataclass
class Constant(Expression):
    constant_type: Type
    value: Union[bool, str, int, float]

    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = [f"\tli $v0, {self.value}\t# load constant value to $v0"]
        return code

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return self.constant_type

def spop(num):
    code = [f"lw   $t{num},0($sp)"]
    code.append("addu $sp,$sp,4")
    return code


def spush(num):
    code = ["subu $sp,$sp,4"]
    code.append(f"sw   $t{num},0($sp)")
    return code


def spop_double(num):
    code = [f"l.d   $f{num},0($sp)"]
    code.append("addu $sp,$sp,8")
    return code


def spush_double(num):
    code = ["subu $sp,$sp,8"]
    code.append(f"s.d   $f{num},0($sp)")
    return code
