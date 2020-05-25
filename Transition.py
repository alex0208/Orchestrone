from AST import AST

class Transition(AST):
    def __init__(self, var=None, formation=None, time=None):
        self.var = var
        self.formation = formation
        self.time = time

    def prettyprint(self):
        if self.var:
            print(self.var, end="")
        else:
            print("new Transition(", end="")
            self.formation.prettyprint()
            print(", {})".format(self.time), end="")

    def fillSymbolTable(self):
        if self.formation:
            return self.formation.fillSymbolTable()
        else:
            print(self)
        pass

    def typeChecking(self):
        pass