from __future__ import annotations

import getopt
import logging
import sys

from .decaf_transformer import DecafTransformer
from .parser import decaf_parser

logging.basicConfig(level=logging.DEBUG)

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
    class Man{
    int b;
    void fat(int b){
        Print(b);
        return;
    }
    }
    class Hi extends Man{
            int j;
            int alo(){
                int x;
                int l;
                j = 540;
                Print(20);
                Print(j);
                l = 999;
                x = 666;
                b = 777;
                Print(x, l, b);
                fat(4);
                return 100;
           
            }
            int halo(){
                Print(this.alo());            
            }
        }
        int main() {
            double a;
            a = 2.2 + 3.5;
            Print(a);
            return 0;
        }
        """
    )
    tree = decaf_parser.parse(
        """
    double hi(int c,double a, int b, double j){
        Print(b);
        Print(c);
        Print(j);
        return a * a;
    }
    int main(){
    int a;
    int b;
    String java;
    a = 100;
    b = 200;
    Print(hi(a, 1.1, b, 100.1));
    Print("HELLO");
    Print("Ola");
    Print("Salam");
    Print("Just let me die please");
    java = ReadLine();
    Print(java);
    java = ReadLine();
    Print(java);
    }"""
    )
    tree = decaf_parser.parse(class_test)
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

"""
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
        /*int[] a;
        Hi k;
        int x;
        a = NewArray(10, int);
        a[2] = 5;
        a[3] = 20;
        Print(a[2], a[3]);
        x =10;
        Print(x);
        Print(a.length());*/
        """
