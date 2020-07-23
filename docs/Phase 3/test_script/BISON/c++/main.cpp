#include <iostream>
#include <fstream>
#include <vector>
#include <string>
using namespace std ;

int main(int argc, char* argv[]){
    if (argc < 5 ){
        cerr<< "Usage: " << argv[0] << " -i <input> -o <output>" << endl ;
        return 1;
    }

    string input_file_name = argv[2];
    string output_file_name = argv[4];

    ofstream output_file("out/" + output_file_name) ;

    output_file << "# PROGRAM: Hello, World!\n"
                << ".data # Data declaration section\n" 
                << "out_string: .asciiz \"Hello, World!\"\n" 
                << ".text # Assembly language instructions\n"
                << "main: # Start of code section\n" 
                << "li $v0, 4 # system call code for printing string = 4\n"
                << "la $a0, out_string # load address of string to be printed into $a0\n"
                << "syscall # call operating system to perform operation in $\n";

}