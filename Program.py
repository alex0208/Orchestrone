from AST import AST
from SymbolTable import SymbolTable
from SymbolTableEntry import SymbolTableEntry

class Program(AST):

    def __init__(self, assignments=None, functions=None):
        super().__init__()
        self.assignments = assignments
        self.functions = functions

    def prettyprint(self):

        for function in self.functions or []:
            function.prettyprint()
            print("")

        for assignment in self.assignments:
            assignment.prettyprint()
            print(";")

    def fillSymbolTable(self):

        if self.functions is not None:
            for function in self.functions:
                entry = SymbolTableEntry(function.id, 'FUNCTION', {'args': function.args, 'asssignments': function.assignments})
                AST.addToSymbolTable(entry)

        for assignment in self.assignments:
            sym_table_entry = assignment.fillSymbolTable()

            if sym_table_entry is not None:
                AST.addToSymbolTable(sym_table_entry)

        return self.symbolTable

    def typeChecking(self):
        pass

    def resolveFuncParams(self):
        print(self)