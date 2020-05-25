from AST import AST


class Calc(AST):
    def __init__(self, operands, operators):
        self.operands = operands
        self.operators = operators

        print(operands)
        print(operators)

    def prettyprint(self):
        for i in range(len(self.operands)):
            if i < len(self.operators):
                print(self.operands[i].value, self.operators[i].value, end=" ")
            else:
                print(self.operands[i].value, end="")

    def fillSymbolTable(self):
        pass

    def typeChecking(self):
        pass
