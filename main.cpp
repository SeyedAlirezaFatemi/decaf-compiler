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
    output_file << "class" << endl ;
    output_file << "T_ID Program" << endl ;
    output_file << "{" << endl ;
    output_file << "void" << endl ;
    output_file << "T_ID main" << endl ;
    output_file << "(" << endl ;
    output_file << ")" << endl ;
    output_file << "{" << endl ;
    output_file << "}" << endl ;
    output_file << "}";

}