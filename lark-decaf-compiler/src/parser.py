from lark import Lark

decaf_parser = Lark(
    grammar=r"""
program: (decl)+ -> finalize

decl: variable_decl -> pass_up_first_element
    | function_decl -> pass_up_first_element
    | class_decl -> pass_up_first_element
    | interface_decl -> pass_up_first_element

variable_decl: variable ";" -> new_variable

variable: type IDENT -> variable_definition

type: PRIM -> pass_up_first_element
    | IDENT -> pass_up_first_element
    | type "[]" -> todo

function_decl: type IDENT "(" formals ")" stmt_block -> new_function
    | "void" IDENT "(" formals ")" stmt_block -> new_void_function

formals: variable ("," variable)* -> pass_up
    | -> pass_up

class_decl: "class" IDENT extend_decl implement_decl "{" (field)* "}" -> new_class

extend_decl: "extends" IDENT -> pass_up_first_element
    | -> pass_up

implement_decl: "implements" IDENT ("," IDENT)* -> pass_up
    | -> pass_up

field: variable_decl -> pass_up_first_element
    | function_decl -> pass_up_first_element

interface_decl: "interface" IDENT "{" (prototype)* "}" -> new_interface

prototype: type IDENT "(" formals ")" ";"
    | "void" IDENT "(" formals ")" ";"

stmt_block: "{" (variable_decl)* (stmt)* "}"

stmt: (expr)? ";"
    | if_stmt
    | while_stmt
    | for_stmt
    | break_stmt
    | return_stmt
    | print_stmt
    | stmt_block

if_stmt: "if" "(" expr ")" stmt ("else" stmt)?

while_stmt: "while" "(" expr ")" stmt

for_stmt: "for" "(" (expr)? ";" expr ";" (expr)? ")" stmt

return_stmt: "return" (expr)? ";"

break_stmt: "break" ";"

print_stmt : "Print" "(" expr ("," expr)* ")" ";"

expr : l_value "=" expr
    | constant
    | l_value
    | "this"
    | call
    | "(" expr ")"
    | expr "+" expr
    | expr "-" expr
    | expr "*" expr
    | expr "/" expr
    | expr "%" expr
    | "-" expr
    | expr "<=" expr
    | expr "<" expr
    | expr ">=" expr
    | expr ">" expr
    | expr "==" expr
    | expr "!=" expr
    | expr "&&" expr
    | expr "||" expr
    | "!" expr
    | "ReadInteger" "(" ")"
    | "ReadLine" "(" ")"
    | "new" IDENT
    | "NewArray" "(" expr "," type ")"

l_value: IDENT
    | expr "." IDENT
    | expr "[" expr "]"

call: IDENT "(" actuals ")"
    | expr "." IDENT "(" actuals ")"

actuals:  expr ("," expr)*
    |

constant: INTEGER
    | DOUBLE
    | BOOL
    | STRING
    | "null"

PRIM: "int"
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
