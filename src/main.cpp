/* File: main.cc
 * -------------
 * This file defines the main() routine for the program and not much else.
 * You should not need to modify this file.
 */
 
#include <cstring>
#include <cstdio>
#include <FlexLexer.h>
#include <fstream>
#include "utility.h"
#include "errors.h"
#include "scanner.h"
#include "location.h"

/* Function: PrintOneToken()
 * Usage: PrintOneToken(T_Double, "3.5", val, loc);
 * -----------------------------------------------
 * We supply this function to print information about the tokens returned
 * by the lexer as part of pp1.  Do not modifiy it.
 */
static void PrintOneToken(TokenType token, const char *text, YYSTYPE value,
                          yyltype loc)
{
  char buffer[] = {'\'', static_cast<char>(token), '\'', '\0'};
  const char *name = token >= T_Void ? gTokenNames[token - T_Void] : buffer;
  
  printf("%-12s line %d cols %d-%d is %s ", text,
	   loc.first_line, loc.first_column, loc.last_column, name);
  
  switch(token) {
    case T_IntConstant:     
      printf("(value = %d)\n", value.integerConstant); break;
    case T_DoubleConstant:   
      printf("(value = %g)\n", value.doubleConstant); break;
    case T_StringConstant:  
      printf("(value = %s)\n", value.stringConstant); break;
    case T_BoolConstant:    
      printf("(value = %s)\n", value.boolConstant ? "true" : "false"); break;
    case T_Identifier:
	if (strcmp(text, value.identifier) != 0) {
	  printf("(truncated to %s)\n", value.identifier);
	  break;
	}
    default:
      printf("\n"); break;
  }
}


/* Function: main()
 * ----------------
 * Entry point to the entire program.  We parse the command line and turn
 * on any debugging flags requested by the user when invoking the program.
 * InitScanner() is used to set up the scanner.
 */
int main(int argc, char *argv[])
{
//    if (argc < 5 ){
//        cerr<< "Usage: " << argv[0] << " -i <input> -o <output>" << endl ;
//        return 1;
//    }

    string input_file_name = "../tests/t01-id1.in";
    string output_file_name = "test.txt";
    std::ifstream my_input_file; // an input file stream object
    std::ofstream my_output_file;
    my_input_file.open(input_file_name);
    my_output_file.open(output_file_name);

//    ParseCommandLine(argc, argv);
    FlexLexer* lexer = new yyFlexLexer(my_input_file, my_output_file);
    cout << lexer->YYLeng();
    InitScanner(lexer);
    TokenType token;
    while ((token = (TokenType)lexer->yylex()) != 0){
        PrintOneToken(token, lexer->YYText(), yylval, yylloc);
    }
    return (ReportError::NumErrors() == 0? 0 : -1);
}
