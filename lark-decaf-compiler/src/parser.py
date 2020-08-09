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
    | -> pass_up_first_element

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

// For operator precedence we write the grammar as follows. From low precedence to high precedence.
// Like this: expr_n: expr_n+1 op expr_n

expr: expr1 "||" expr -> logical_or
    | assignment -> pass_up_first_element
    | expr1 -> pass_up_first_element

expr1: expr2 "&&" expr1 -> logical_and
    | expr2 -> pass_up_first_element

expr2: expr3 "==" expr2 -> equals_operation
    | expr3 -> pass_up_first_element

expr3: expr4 "!=" expr3 -> not_equals_operation
    | expr4 -> pass_up_first_element

expr4: expr5 "<" expr4 -> lt_operation
    | expr5 -> pass_up_first_element

expr5: expr6 "<=" expr5 -> lte_operation
    | expr6 -> pass_up_first_element

expr6: expr7 ">" expr6 -> gt_operation
    | expr7 -> pass_up_first_element

expr7: expr8 ">=" expr7 -> gte_operation
    | expr8 -> pass_up_first_element

expr8: expr9 "+" expr8 -> addition_operation
    | expr9 -> pass_up_first_element

expr9: expr9 "-" expr10 -> subtraction_operation
    | expr10 -> pass_up_first_element

expr10: expr11 "*" expr10 -> multiplication_operation
    | expr11 -> pass_up_first_element

expr11: expr11 "/" expr12 -> division_operation
    | expr12 -> pass_up_first_element

expr12: expr12 "%" expr13 -> modulo_operation
    | expr13 -> pass_up_first_element

expr13: "-" expr14 -> minus_operation
    | expr14 -> pass_up_first_element

expr14: "!" expr15 -> not_operation
    | expr15 -> pass_up_first_element

expr15: "(" expr ")" -> pass_up_first_element
    | constant -> pass_up_first_element
    | l_value -> pass_up_first_element
    | "this" -> this_expression
    | call -> pass_up_first_element
    | "ReadInteger" "(" ")" -> read_integer
    | "ReadLine" "(" ")" -> read_line
    | "new" identifier -> initiate_class
    | "NewArray" "(" expr "," type ")" -> initiate_array

assignment: l_value "=" expr -> assignment

l_value: identifier -> identifier_l_value
    | expr15 "." identifier -> member_access_l_value
    | expr15 "[" expr "]" -> array_access_l_value

call: identifier "(" actuals ")" -> function_call
    | expr15 "." identifier "(" actuals ")" -> method_call

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
