from __future__ import annotations

import getopt
import logging
import sys

from .decaf_transformer import DecafTransformer
from .parser import decaf_parser

logging.basicConfig(level=logging.DEBUG)


def main(argv):
    tree = decaf_parser.parse(
        """
    int main(int a, int b, int c) {
    int a;
    }
    void hi() {
    }
    class Person implements Nameable {
    string name;

    void setName(string new_name) {
        name = new_name;
    }

    string getName() {
        return name;
    }

    int age;

    void setAge(int new_age) {
        age = new_age;
    }

    int getAge() {
        return age;
    }

    void print() {
        Print("Name: ", name, " Age: ", age);
    }
}
class HELLO{}
"""
    )
    tree = decaf_parser.parse(
        """
    int a;
    int b;
    class HELLO{
        int getAge() {}
    }
    int getAge() {
        for (;x<0;){
        }
        Print(1, 2, 3);
        return;
    }
"""
    )
    tree = decaf_parser.parse(
        """
        int i;
        int b;
    int main() {
        /*int i;
        for(i = 1; i < 5; i = i + 1) {
        Print(1);
        }*/
        /*i = 0;
        Print(i);
        i = 100;
        Print(i);
        b = i + 40;
        Print(b);
        Print(10 + 10 * 10);*/
        int[] a;
        int x;
        a = NewArray(10, int);
        a[2] = 5;
        a[3] = 20;
        Print(a[2], a[3]);
        x =10;
        Print(x);
        Print(a.length());
    }
"""
    )
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
