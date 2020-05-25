import sys
from drone_parser import Parser
from lexer import Lexer
from SymbolTable import SymbolTable
from compiler import Compiler

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        filename = "example"
    else:
        filename = sys.argv[1]

    f = open(filename, "r")
    source = f.read()

    # Lexer setup
    lexer = Lexer(source)
    tokens = lexer.getAllTokens()

    # Parser setup
    parser = Parser(source, tokens)
    ast = parser.Program()

    # Symbol table filling
    symTable = ast.fillSymbolTable()
    compiled = Compiler(ast.instructionsTable)

    # Print the generated UDP commands
    print(compiled.udp_commands)