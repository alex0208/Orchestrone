from AST import AST


class Drone(AST):
    def __init__(self, ip):
        self.ip = ip

    def prettyprint(self):
        print("new Drone({})".format(self.ip), end="")

    def fillSymbolTable(self):
        return self.ip

    def typeChecking(self):
        pass
