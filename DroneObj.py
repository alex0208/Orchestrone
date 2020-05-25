from AST import AST

class DroneObj(AST):
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def prettyprint(self):
        print("{","drone: {}, x: {}, y: {}"
            .format(self.id, self.x, self.y),
            "}", end="")

    def fillSymbolTable(self):
        return self.id, self.x, self.y

    def typeChecking(self):
        pass