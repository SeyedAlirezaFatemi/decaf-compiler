from dataclasses import dataclass
from typing import List, Union, Any, Optional, Dict

from lark import Transformer, Tree, Token

variable_size = {"int": 4, "string": 100, "double": 8, "bool": 4}


@dataclass
class Variable:
    name: str
    type: str


@dataclass
class NodeOutput:
    code: str
    address: Any


class DecafTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.variable_map = dict()
        self.stack_pointer = 0x7FFFFFFF

    def pass_up(self, args):
        return args

    def pass_up_first_element(self, args):
        return args[0]

    def new_variable(self, args):
        # Here, we should take space for the variable and insert it to the spaghetti stack
        print("new_variable")
        print(args)
        return args[0]

    def variable_definition(self, args):
        print("variable_definition", args)
        variable_type = args[0]
        variable_name = args[1]
        return Variable(variable_name, variable_type)

    def new_function(self, args: List[Union[Tree, Token]]):
        print("new_function")
        print(args)
        return_type = args[0]
        function_name = args[1]
        function_parameters = args[2]

    def new_void_function(self, args):
        print("new_void_function")
        print(args)
        function_name = args[0]
        function_parameters = args[1]

    def new_class(self, args):
        print("new_class")
        print(args)
        class_name = args[0]

    def new_interface(self, args):
        print("new_interface")
        print(args)

    def finalize(self, args):
        pass

    def print(self, args):
        """
        Page A-49
        Code is inside standard_library_functions.py
        print_int 01 $a0 = integer
        print_float 02 $f12 = float
        print_double 03 $f12 = double
        print_string 04 $a0 = string
        """
        # TODO: Call
        pass

    def read_integer(self, args):
        """
        Page A-49
        Code is inside standard_library_functions.py
        read_int 05 integer (in $v0)
        """
        # TODO: Call
        pass



class Node:
    pass

class Declaration(Node):
    identifier: Identifier


class Identifier(Node):
    name: str
    declrations: Declaration

class Scope:
    name_declaration_map: Dict[str, Declaration]
    parent_scope: Optional[Scope]
    parent_class_name: Opional[str]
    owner_class_name: Opional[str]

    def __init__(self, parent_scope: Optional[Scope]= None, parent_class_name: Optional[str] = None, owner_class_name: Optional[str]):
        self.name_declaration_map = dict()
        self.parent_scope = parent_scope
        self.parent_class_name = parent_class_name
        self.owner_class_name = owner_class_name
    
    def lookup(self, name):
        if name in self.name_declaration_map:
            return self.name_declaration_map[name]
        if self.parent_scope is None:
            print("Error")
        else:
            return self.parent_scope.lookup(name)

    def add_declaration(self, decleration: Declaration):
        self.name_declaration_map[decleration.identifier.name] = decleration


class SymbolTable:
    global_scope: Scope
    current_scope: Scope

    def __init__(self):
        # init global scope
        self.global_scope = Scope()
        self.current_scope = self.global_scope
    
    def enter_new_scope(self, owner_class_name: Optional[str] = None):
        new_scope = Scope(self.current_scope, owner_class_name=owner_class_name)
        self.current_scope = new_scope

    def exit_current_scope(self):
        prev_scope = self.current_scope
        self.current_scope = self.current_scope.parent_scope
        del prev_scope

    def add_declaration_to_global_scope(self, decleration: Declaration):
        self.global_scope.add_declaration(decleration)
        
    def add_declaration_to_current_scope(self, decleration: Declaration):
        self.current_scope.add_declaration(decleration)


class Type(Node):
    name: str

class NamedType(Node):
    identifier: Identifier

class ArrayType(Type):
    elementType: Type

class VariableDecleration(Declaration):
    variable_type: Type
    is_global: bool
    class_member_offset: int

class ClassDecleration(Declaration):
    members: List[Declaration]
    extends: NamedType
    intstance_size: int
    vtable_size: int
    variable_members: List[VariableDecleration]
    methods: List[FunctionDecleratoin]

class FunctionDecleratoin(Declaration):
    formal_parameters: List[VariableDecleration]
    return_type: Type
    body: Statement

class Program(Node):
    declarations: List[Declaration]


class Expression(Node):
    pass


class Statement(Node):
    pass

class StatementBlock(Statement):
    variable_declarations: List[VariableDecleration]
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
