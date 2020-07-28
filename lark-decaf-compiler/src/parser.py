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

type: PRIM -> pass_up_first_element
    | identifier -> pass_up_first_element
    | type "[]" -> todo

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

stmt_block: "{" (variable_decl)* (stmt)* "}"

stmt: (expr)? ";"
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

print_stmt : "Print" "(" expr ("," expr)* ")" ";" -> print

expr : assignment
    | constant
    | l_value
    | "this"
    | call
    | "(" expr ")"
    | minus
    | not
    | multiplication
    | division
    | modulo
    | addition
    | subtraction
    | inequality
    | equality
    | logical_and
    | logical_or
    | "ReadInteger" "(" ")" -> read_integer
    | "ReadLine" "(" ")"
    | "new" identifier
    | "NewArray" "(" expr "," type ")"

minus.8: "-" expr -> minus
not.8: "!" expr -> not 
multiplication.7: expr "*" expr -> multiplication
division.7: expr "/" expr -> division
modulo.7: expr "%" expr -> modulo
addition.6: expr "+" expr -> addition 
subtraction.6: expr "-" expr -> subtraction
inequality.5: expr "<=" expr -> inequality 
    | expr "<" expr -> inequality
    | expr ">=" expr -> inequality
    | expr ">" expr -> inequality
equality.5: expr "==" expr -> equality
    | expr "!=" expr -> equality
logical_and.4: expr "&&" expr -> logical_and 
logical_or.4: expr "||" expr -> logical_or
assignment: l_value "=" expr -> assignment

l_value: identifier
    | expr "." identifier
    | expr "[" expr "]"

call: identifier "(" actuals ")"
    | expr "." identifier "(" actuals ")"

actuals:  expr ("," expr)*
    |

identifier: IDENT -> identifier
new_identifier: IDENT -> new_identifier

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
