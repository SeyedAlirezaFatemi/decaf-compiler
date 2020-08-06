from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List

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

def spop(self, num):
    code = [f"lw   $t{num},0($sp)"]
    code.append("addu $sp,$sp,4")
    return code

def spush(self, num):
    code = ["subu $sp,$sp,4"]
    code.append(f"sw   $t{num},0($sp)")
    return code

def spop_double(self, num):
    code = [f"l.d   $f{num},0($sp)"]
    code.append("addu $sp,$sp,8")
    return code

def spush_double(self, num):
    code = ["subu $sp,$sp,8"]
    code.append(f"s.d   $f{num},0($sp)")
    return code

@dataclass
class BinaryExpression(Expression):
    operator: Operator
    left_expression: Expression
    right_expression: Expression

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        # TODO: based on operators and left and right expression
        pass
    
    def generate_code(self, symbol_table: SymbolTable) -> List[str]:
        code = []
        code += left_expression.generate_code()
        code += right_expression.generate_code()
        if operator == Operator.ADDITION:
            if self.evaluate_type(SymbolTable) == 
                code += spop(0)
                code += spop(1)
                code.append('addu $t0,$t0,$t1')
                code += spush(0)
            else:
                code += spop_double(0)
                code += spop_double(2)
                code.append('add.d $f4, $f2, $f0')
                code += spush_double(4)
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
        return NamedType(class_decl.identifier.name, class_decl.identifier)


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
        return NamedType(self.class_identifier.name, self.class_identifier)


@dataclass
class InitiateArray(Expression):
    length_expression: Expression
    element_type: Type

    def evaluate_type(self, symbol_table: SymbolTable) -> Type:
        return ArrayType(self.element_type.name, self.element_type)
