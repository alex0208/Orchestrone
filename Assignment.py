from AST import AST
from SymbolTableEntry import SymbolTableEntry


class Assignment(AST):
    def __init__(self, id, cmd=None, expr=None):
        super().__init__()

        self.id = id
        self.cmd = cmd
        self.expr = expr

    def prettyprint(self):
        if self.expr:
            print("{} = ".format(self.id), end="")
            self.expr.prettyprint()
        else:
            print("{}.".format(self.id), end="")
            self.cmd.prettyprint()

    def fillSymbolTable(self):
        if self.expr:
            expr_type, expr_value = self.expr.fillSymbolTable()
            return SymbolTableEntry(self.id, expr_type, expr_value)
        else:
            self.cmd.generateInstruction()

    def typeChecking(self):
        pass
