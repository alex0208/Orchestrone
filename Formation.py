from AST import AST

class Formation(AST):
    def __init__(self, var=None, drones_list=None):
        super().__init__()

        self.var = var
        self.drones_list = drones_list

    def prettyprint(self):
        if self.var:
            print(self.var, end="")
        else:
            print("new Formation([", end="")
            for drone in self.drones_list:
                drone.prettyprint()
            print("])", end="")

    def fillSymbolTable(self):
        # change names of drone and drone list to coordinates
        if self.drones_list is not None:
            formation = []
            for drone in self.drones_list:
                formation.append(drone.fillSymbolTable())
            return formation

        if self.var:
            tableEntry = AST.getEntry(self.var)
            if tableEntry is not None:
                return tableEntry.value
            raise Exception('Undefined variable ' + self.var)


    def typeChecking(self):
        pass

