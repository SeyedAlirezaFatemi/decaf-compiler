#include <cstring>
#include <FlexLexer.h>
#include <fstream>
#include "iostream"
#include "errors.h"
#include "scanner.h"
#include "location.h"
#include "utility.h"

/* Function: PrintOneToken()
 * Usage: PrintOneToken(T_Double, "3.5", val, loc);
 * -----------------------------------------------
 * We supply this function to print information about the tokens returned
 * by the lexer.
 */
static void PrintOneToken(std::ofstream &output_file, TokenType token, const char *text, YYSTYPE value,
                          yyltype loc) {
    char buffer[] = {'\'', static_cast<char>(token), '\'', '\0'};
    const char *name = token >= T_Void ? gTokenNames[token - T_Void] : buffer;

    printf("%-12s line %d cols %d-%d is %s ", text,
           loc.first_line, loc.first_column, loc.last_column, name);

    switch (token) {
        case T_IntConstant:
            output_file << "T_INTLITERAL " << text << endl;
            printf("(value = %d)\n", value.integerConstant);
            break;
        case T_DoubleConstant:
            output_file << "T_DOUBLELITERAL " << text << endl;
            printf("(value = %g)\n", value.doubleConstant);
            break;
        case T_StringConstant:
            output_file << "T_STRINGLITERAL " << value.stringConstant << endl;
            printf("(value = %s)\n", value.stringConstant);
            break;
        case T_BoolConstant:
            output_file << "T_BOOLEANLITERAL " << (value.boolConstant ? "true" : "false") << endl;
            printf("(value = %s)\n", value.boolConstant ? "true" : "false");
            break;
        case T_Identifier:
            if (strcmp(text, value.identifier) != 0) {
                printf("(truncated to %s)\n", value.identifier);
                break;
            }
            output_file << "T_ID " << text << endl;
            printf("\n");
            break;
        default:
            output_file << text << endl;
            printf("\n");
            break;
    }
}


/* Function: main()
 * ----------------
 * Entry point to the entire program.  We parse the command line and turn
 * on any debugging flags requested by the user when invoking the program.
 * InitScanner() is used to set up the scanner.
 */
int main(int argc, char *argv[]) {
    if (argc < 5) {
        cerr << "Usage: " << argv[0] << " -i <input> -o <output>" << endl;
        return 1;
    }

    string input_file_name = argv[2];
    string output_file_name = argv[4];
//    string input_file_name = "../tests/t07-operator1.in";
//    string output_file_name = "../out/test.txt";

    std::ifstream my_input_file(input_file_name);
    std::ofstream my_output_file(output_file_name);

//    ParseCommandLine(argc, argv);
    FlexLexer *lexer = new yyFlexLexer(my_input_file, my_output_file);
    cout << lexer->YYLeng();
    InitScanner(lexer);
    TokenType token;
    while ((token = (TokenType) lexer->yylex()) != 0) {
        PrintOneToken(my_output_file, token, lexer->YYText(), yylval, yylloc);
    }
    my_output_file.flush();
    my_output_file.close();
//    return (ReportError::NumErrors() == 0 ? 0 : -1);
    return 0;
}
