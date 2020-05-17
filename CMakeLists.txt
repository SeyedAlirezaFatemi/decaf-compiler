cmake_minimum_required(VERSION 3.16)
project(decaf_compiler)

set(CMAKE_CXX_STANDARD 20)

add_executable(decaf_compiler
        src/main.cpp
        src/errors.cpp
        src/utility.cpp
        src/scanner.h
        src/location.h
        src/errors.h
        src/lex.yy.cc)
