from AST import AST

class Group(AST):
    def __init__(self, formation):
        self.formation = formation

    def prettyprint(self):
        print("new Group(", end="")
        self.formation.prettyprint()
        print(")", end="")

    def fillSymbolTable(self):
        return self.formation.fillSymbolTable()

    def typeChecking(self):
        pass