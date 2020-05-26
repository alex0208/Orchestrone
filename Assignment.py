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

            if AST.getEntry(self.id) is not None:
                if AST.getEntry(self.id).type != expr_type:
                    raise Exception('Error when trying to assign type {0} to {1}'.format(expr_type, AST.getEntry(self.id).type))
            return SymbolTableEntry(self.id, expr_type, expr_value)
        else:
            self.cmd.generateInstruction()

    def typeChecking(self):
        pass
