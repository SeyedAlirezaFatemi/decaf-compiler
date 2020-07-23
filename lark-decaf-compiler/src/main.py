import getopt
import logging
import sys

from .decaf_transformer import DecafTransformer
from .parser import decaf_parser

logging.basicConfig(level=logging.DEBUG)


def main(argv):
    tree = decaf_parser.parse("""
    int main(int a, int b, int c) {
    int a;
    }
    void hi() {
    }""")
    DecafTransformer().transform(tree)
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
        # for the sake of testing :
        output_file.write("YES" if success else "NO")


if __name__ == "__main__":
    main(sys.argv[1:])
