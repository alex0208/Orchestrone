from AST import AST

class Function(AST):
    def __init__(self, id, args, assignments):
        super().__init__()

        self.id = id
        self.args = args
        self.assignments = assignments

    def prettyprint(self):
        print("function {}({})".format(self.id, ", ".join(self.args)), end="")
        print("{")

        for assignment in self.assignments:
            print("\t", end="")
            assignment.prettyprint()
            print(";")

        print("}")

    def fillSymbolTable(self):
        func_args =  self.args

        for assignment in self.assignments:
            temp = assignment.fillSymbolTable()

    def typeChecking(self):
        pass