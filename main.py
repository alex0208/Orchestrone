import sys
import time

from drone_parser import Parser
from lexer import Lexer
from SymbolTable import SymbolTable
from compiler import Compiler

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        filename = "test_example"
    else:
        filename = sys.argv[1]

    print("Start parsing file", filename)
    f = open(filename, "r")
    source = f.read()

    # Lexer setup
    lexer = Lexer(source)
    tokens = lexer.getAllTokens()
    print("Lexical parsing successful")

    start = time.time()
    # Parser setup
    parser = Parser(source, tokens)
    ast = parser.Program()
    finish = time.time()

    print("")
    print("Parsing successful in {} seconds".format((finish - start)))

    print("")
    print("Trying to pretty-print the code from AST")
    print("")
    ast.prettyprint()

    print("")
    print("###########################################################")

    # Symbol table filling
    symTable = ast.fillSymbolTable()

    for key, value in symTable.getTable().items(): print(value)

    # print(list(ast.instructionsTable))
    print("")
    print("###########################################################")

    for instr in ast.instructionsTable: print(instr)

    print("")
    print("###########################################################")
    compiled = Compiler(ast.instructionsTable)
    print(compiled.udp_commands)