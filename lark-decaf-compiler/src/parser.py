from lark import Lark

decaf_parser = Lark(
    grammar=r"""
program: (decl)+ -> finalize

decl: variable_decl -> pass_up_first_element
    | function_decl -> pass_up_first_element
    | class_decl -> pass_up_first_element
    | interface_decl -> pass_up_first_element

variable_decl: variable ";" -> new_variable

variable: type new_identifier -> variable_definition

type: PRIM -> prim_type
    | identifier -> named_type
    | type "[]" -> array_type

function_decl: type new_identifier "(" formals ")" stmt_block -> new_function
    | "void" new_identifier "(" formals ")" stmt_block -> new_void_function

formals: variable ("," variable)* -> pass_up
    | -> pass_up

class_decl: "class" new_identifier extend_decl implement_decl "{" fields_decl "}" -> new_class

extend_decl: "extends" identifier -> pass_up_first_element
    | -> pass_up

implement_decl: "implements" identifier ("," identifier)* -> pass_up
    | -> pass_up

fields_decl: (field)* -> pass_up

field: variable_decl -> pass_up_first_element
    | function_decl -> pass_up_first_element

interface_decl: "interface" new_identifier "{" (prototype)* "}"

prototype: type new_identifier "(" formals ")" ";"
    | "void" new_identifier "(" formals ")" ";"

stmt_block: "{" (variable_decl)* (stmt)* "}" -> statement_block

stmt: optional_expression ";" -> optional_expresion_statement
    | if_stmt -> pass_up_first_element
    | while_stmt -> pass_up_first_element
    | for_stmt -> pass_up_first_element
    | break_stmt -> pass_up_first_element
    | return_stmt -> pass_up_first_element
    | print_stmt -> pass_up_first_element
    | stmt_block -> pass_up_first_element

if_stmt: "if" "(" expr ")" stmt ("else" stmt)? -> if_statement

while_stmt: "while" "(" expr ")" stmt -> while_statement

for_stmt: "for" "(" optional_expression ";" expr ";" optional_expression ")" stmt -> for_statement

return_stmt: "return" optional_expression ";" -> return_statement

optional_expression: (expr)? -> pass_up_first_element

break_stmt: "break" ";" -> break_statement

print_stmt : "Print" "(" expr ("," expr)* ")" ";" -> print_statement

expr : assignment -> pass_up_first_element
    | constant -> pass_up_first_element
    | l_value -> pass_up_first_element
    | "this" -> this_expression
    | call -> pass_up_first_element
    | "(" expr ")" -> pass_up_first_element
    | minus -> pass_up_first_element
    | not -> pass_up_first_element
    | multiplication -> pass_up_first_element
    | division -> pass_up_first_element
    | modulo -> pass_up_first_element
    | addition -> pass_up_first_element
    | subtraction -> pass_up_first_element
    | inequality -> pass_up_first_element
    | equality -> pass_up_first_element
    | logical_and -> pass_up_first_element
    | logical_or -> pass_up_first_element
    | "ReadInteger" "(" ")" -> read_integer
    | "ReadLine" "(" ")" -> read_line
    | "new" identifier -> initiate_class
    | "NewArray" "(" expr "," type ")" -> initiate_array

minus.8: "-" expr -> minus_operation
not.8: "!" expr -> not_operation

multiplication.7: expr "*" expr -> multiplication_operation
division.7: expr "/" expr -> division_operation
modulo.7: expr "%" expr -> modulo_operation
addition.6: expr "+" expr -> addition_operation
subtraction.6: expr "-" expr -> subtraction_operation
inequality.5: expr "<=" expr -> lte_operation
    | expr "<" expr -> lt_operation
    | expr ">=" expr -> gte_operation
    | expr ">" expr -> gt_operation
equality.5: expr "==" expr -> equals_operation
    | expr "!=" expr -> not_equals_operation
logical_and.4: expr "&&" expr -> and_operation 
logical_or.4: expr "||" expr -> or_operation

assignment: l_value "=" expr -> assignment

l_value: identifier -> identifier_l_value
    | expr "." identifier -> member_access_l_value
    | expr "[" expr "]" -> array_access_l_value

call: identifier "(" actuals ")" -> function_call
    | expr "." identifier "(" actuals ")" -> method_call

actuals:  expr ("," expr)* -> pass_up
    | -> pass_up

identifier: IDENT -> identifier
new_identifier: IDENT -> new_identifier

constant: INTEGER -> int_const
    | DOUBLE -> double_const
    | BOOL -> bool_const
    | STRING -> string_const
    | "null" -> null_const

PRIM.2: "int"
    | "double"
    | "bool"
    | "string"

BOOL.2: "true"
    | "false"
DOUBLE.2: /(\d)+\.(\d)*(([Ee])(\+|\-)?(\d)+)?/
IDENT: /[a-zA-Z][a-zA-Z0-9_]{0,30}/
STRING : /"(?:[^\\"]|\\.)*"/
HEXADECIMAL: /0[xX][0-9a-fA-F]+/
DECIMAL: /[0-9]+/
INTEGER: HEXADECIMAL
    | DECIMAL

INLINE_COMMENT : /\/\/.*/
MULTILINE_COMMENT : /\/\*(\*(?!\/)|[^*])*\*\//
%ignore INLINE_COMMENT
%ignore MULTILINE_COMMENT

%import common.WS
%ignore WS
""",
    start="program",
    parser="lalr",
)
