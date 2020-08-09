from __future__ import annotations

import getopt
import logging
import sys

from .decaf_transformer import DecafTransformer
from .parser import decaf_parser
from .standard_library_functions import standard_library_functions

logging.basicConfig(level=logging.DEBUG)

op_test = """
int main(){
    bool a;
    a = itob(0);
    Print(a);
}"""
array_test = """
int main() {
    int[] k;
    int[] b;
    k = NewArray(10, int);
    k[5] = 20;
    k[4] = 112;
    b = k;
    Print(k[4], k[5]);
    Print(b[4], b[5]);
}
"""

class_test = """
double gd;
class Greet{
    double ggg;
    int brother(){
    Print("In Brother");
    ggg = 21381.0;
    Print(ggg);
    return 8490;
    }
}
class Hi extends Greet{
    int j;
    int aba;
    int alo(){
        this.j = 540;
        this.aba = 90000;
        gd = 500.0;
        Print(j);
        Print(aba);
        this.go();
        Print(j);
        brother();
        Print("After brother");
        //ggg = 200.0;
        Print(ggg);
        return 2;
    }
    int go(){
        this.j = 400;
        return 2;
    }
}
int main() {
    Hi k;
    double kl;
    k = new Hi;
    kl = 8909.0;
    Print(k.alo());
    Print(gd);
    Print(kl);
}
"""

string_test = """
int main(){
    string a;
    a = "alireza";
    a = ReadLine();
    Print(a);
}"""


def main(argv):
    tree = decaf_parser.parse(op_test)
    code = DecafTransformer().transform(tree)
    return
    inputfile = ""
    outputfile = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("main.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    success = True
    with open("tests/" + inputfile, "r") as input_file:

        try:
            tree = decaf_parser.parse(input_file.read())
            DecafTransformer().transform(tree)
        except BaseException as e:
            # print(e)
            success = False

    with open("out/" + outputfile, "w") as output_file:
        # write result to output file.
        print("\n".join(code), file=output_file)
        print(standard_library_functions, file=output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
