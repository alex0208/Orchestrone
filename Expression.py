from AST import AST

class Expression(AST):
    def __init__(self, obj=None, term=None):
        # Separate instance vars to know what object type it is
        self.obj = obj
        self.term = term

    def prettyprint(self):
        if self.obj:
            self.obj.prettyprint()
        else:
            self.term.prettyprint()

    def fillSymbolTable(self):
        if self.obj:
            etype = self.obj.getType()
            values = self.obj.fillSymbolTable()
            return etype, values
        elif self.term:
            ttype = self.term.type if self.term.type is not None else 'LIST'
            tvalues = self.term.fillSymbolTable()
            return ttype, tvalues

    def typeChecking(self):
        pass