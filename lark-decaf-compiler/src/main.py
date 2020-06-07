from lark import Lark

decaf_parser = Lark(grammar="""
program: (decl)+
decl: variable_decl
    | function_decl
    | class_decl
    | interface_decl
variable_decl: variable ";"
variable: type IDENT
type: "int"
    | "double"
    | "bool"
    | "string"
    | IDENT
    | type "[]"
function_decl: type IDENT "(" formals ")" stmt_block
    | "void" IDENT "(" formals ")" stmt_block
formals: variable ("," variable)*
    |
class_decl: "class" IDENT ("extends" IDENT)? ("implements" IDENT ("," IDENT)*)? "{" (field)* "}"
field: variable_decl
    | function_decl
interface_decl: "interface" IDENT "{" (prototype)* "}"
prototype: type IDENT "(" formals ");"
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

%import common.WS
%ignore WS
""", start="program")
