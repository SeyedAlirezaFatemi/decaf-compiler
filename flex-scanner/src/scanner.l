/* File:  scanner.l
 * ----------------
 * Lex input file to generate the scanner for the compiler.
 */

%{

/* The text within this first region delimited by %{ and %} is assumed to
 * be C/C++ code and will be copied verbatim to the lex.yy.c file ahead
 * of the definitions of the yylex() function. Add other header file inclusions
 * or C++ variable declarations/prototypes that are needed by your code here.
 */

#include <string.h>
#include <ctype.h>
#include "scanner.h"
#include "utility.h" // for PrintDebug()
#include "errors.h"


/* Global variable: yylval
 * -----------------------
 * This global variable is how we get attribute information about the token
 * just scanned to the client. The scanner sets the global variable
 * appropriately and since it's global the client can just read it.
 */
YYSTYPE yylval;

/* Global variable: yylloc
 * -----------------------
 * This global variable is how we get position information about the token
 * just scanned to the client. (Operates similarly to yylval above)
 */
struct yyltype yylloc; // manually dclared for pp1, later Yacc provides

/* Macro: YY_USER_ACTION 
 * ---------------------
 * This flex built-in macro can be defined to provide an action which is
 * always executed prior to any matched rule's action. Basically, it is
 * a way of having a piece of code common to all actions factored out to
 * this routine.  We already defined it for you and left the empty
 * function DoBeforeEachAction ready for your use as needed. It will
 * be called once for each pattern scanned from the file, before
 * executing its action.
 */
static void DoBeforeEachAction(); 
#define YY_USER_ACTION DoBeforeEachAction();

#define TAB_SIZE 8

int line_number, colno;
FlexLexer* currentLexer;
%}

 /* The section before the first %% is the Definitions section of the lex
  * input file. Here is where you set options for the scanner, define lex
  * states, and can set up definitions to give names to regular expressions
  * as a simple substitution mechanism that allows for more readable
  * entries in the Rules section later. 
  */
PUNCTUATION        ([!;,.[\]{}()])
ARITHMETIC         ([-+*/%])
RELATIONAL         ([<>=])
OPERATOR           ({ARITHMETIC}|{RELATIONAL})
DECIMAL            ([0-9]+)
HEXADECIMAL        (0[xX][0-9a-fA-F]+)
CHARS              (\"[^\"\n]*\")
BOOLEAN            (true|false)   
INTEGER            ({DECIMAL}|{HEXADECIMAL})   
FLOAT              ({DECIMAL}\.{DECIMAL}?((E|e)(\+|\-)?{DECIMAL})?)
IDENTIFIER         ([a-zA-Z][a-zA-Z0-9_]*)

%x COMMENT
%option noyywrap
%%             /* BEGIN RULES SECTION */
 /* All patterns and actions should be placed between the start and stop
  * %% markers which delimit the Rules section. 
  */ 

 /* skip over white space */
[\n]                   { colno = 1; line_number++; }
[\t]                   { colno += TAB_SIZE - colno % TAB_SIZE + 1; }
[ ]                    ;

 /* recognize all keywords and return the correct token from scanner.h */
void                   { return T_Void; }
int                    { return T_Int; }
double                 { return T_Double; }
bool                   { return T_Bool; }
string                 { return T_String; }
class                  { return T_Class; }
interface              { return T_Interface; }
null                   { return T_Null; }
this                   { return T_This; }
extends                { return T_Extends; }
implements             { return T_Implements; }
for                    { return T_For; }
while                  { return T_While; }
if                     { return T_If; }
else                   { return T_Else; }
return                 { return T_Return; }
break                  { return T_Break; }
new                    { return T_New; }
NewArray               { return T_NewArray; }
Print                  { return T_Print; }
ReadInteger            { return T_ReadInteger; }
ReadLine               { return T_ReadLine; }

 
 /* recognize punctuation and single-char operators 
  * and return the ASCII value as the token 
  */
{PUNCTUATION} |
{OPERATOR}             { return YYText()[0]; }


 /* recognize two-character operators and return the correct token */
\<=                    { return T_LessEqual; }
\>=                    { return T_GreaterEqual; }
==                     { return T_Equal; }
!=                     { return T_NotEqual; }
\[\]                   { return T_Dims; }
&&                     { return T_And; }
\|\|                   { return T_Or; }

 /* recognize int, double, bool and string constants,
  * return the correct token
  * and set appropriate filed of yylval 
  */
{CHARS}                  { 
                           yylval.stringConstant = strdup(YYText());
                           return T_StringConstant;
                         }
{BOOLEAN}                { 
                           if (strcmp("true", YYText()) == 0)
                              yylval.boolConstant = true;
                           else
			                        yylval.boolConstant = false;
                           return T_BoolConstant;
                         }
{DECIMAL}                { 
                           yylval.integerConstant = strtol(YYText(), NULL, 10); return T_IntConstant;
		                 }
{HEXADECIMAL}            {
                          yylval.integerConstant = strtol(YYText(), NULL, 16);
			                    return T_IntConstant;
                         }
{FLOAT}                  { 
                           yylval.doubleConstant = atof(YYText()); return T_DoubleConstant;
			             }

 /* recognize identifiers, 
  * return the correct token and set appropriate fields of yylval 
  */
{IDENTIFIER}             { 
                          if (yyleng > MaxIdentLen)
        	                  ReportError::LongIdentifier(&yylloc, YYText());
                          strncpy(yylval.identifier, YYText(), MaxIdentLen);
                          yylval.identifier[MaxIdentLen] = '\0';   
                          
                          return T_Identifier;
                         }

 /* consume single-line comment */
\/\/.*\n                { 
                          line_number++; 
                          colno = 1;
                        }
\/\*.*\*\/              ;

 /* consume multi-line comments 
  * report unterminated comment
  */

\/\*                    { BEGIN COMMENT; }
<COMMENT>.              ;
<COMMENT>[\r\n]         { 
                          line_number++; 
                          colno = 1;
			            }
<COMMENT>\*\/           { BEGIN INITIAL; }
<COMMENT><<EOF>>        { 
                          ReportError::UnterminatedComment();
                          BEGIN INITIAL;
                        }

 /* report lexical error for improper strings 
  * and invalid characters
  */
\"[^\"\n]*\n            { 
                          ReportError::UnterminatedString(&yylloc, YYText());
                          line_number++;
                          colno = 1;
                        }

 /* all other characters are reported as errors */
.                       { 
                          ReportError::UnrecognizedChar(&yylloc, YYText()[0]);
			            }

%%
/* The closing %% above marks the end of the Rules section and the beginning
 * of the User Subroutines section. All text from here to the end of the
 * file is copied verbatim to the end of the generated lex.yy.c file.
 * This section is where you put definitions of helper functions.
 */


/* Function: InitScanner
 * ---------------------
 * This function will be called before any calls to yylex().  It is designed
 * to give you an opportunity to do anything that must be done to initialize
 * the scanner (set global variables, configure starting state, etc.). One
 * thing it already does for you is assign the value of the global variable
 * yy_flex_debug that controls whether flex prints debugging information
 * about each token and what rule was matched. If set to false, no information
 * is printed. Setting it to true will give you a running trail that might
 * be helpful when debugging your scanner.
 */
void InitScanner(FlexLexer* lexer)
{
    PrintDebug("lex", "Initializing scanner");
    line_number = 1;
    colno = 1;
    currentLexer = lexer;
}


/* Function: DoBeforeEachAction()
 * ------------------------------
 * This function is installed as the YY_USER_ACTION. This is a place
 * to group code common to all actions.
 */
static void DoBeforeEachAction()
{
  yylloc.first_line = yylloc.last_line = line_number;

  yylloc.first_column = colno;
  yylloc.last_column = colno + currentLexer->YYLeng() - 1;
  colno = colno + currentLexer->YYLeng();
}
