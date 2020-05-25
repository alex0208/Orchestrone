from SymbolTable import SymbolTable

class AST(object):

    symbolTable = SymbolTable()
    instructionsTable = []

    def __init__(self):
        self.code = ""

    def prettyprint(self):
        pass

    def fillSymbolTable(self):
        pass

    def typeChecking(self):
        pass

    def emit(self, string):
        self.code += string

    def getType(self):
        return self.__class__.__name__

    def lookupVar(self, identifier):
        print(self)
        print(identifier)

    @staticmethod
    def addToSymbolTable(entry):
        AST.symbolTable.addToSymbolTable(entry)

    def getTable(self):
        return self.__table

    @staticmethod
    def getTableEntries():
        return AST.symbolTable.getTable()

    @staticmethod
    def isTermTaken(term):
        if AST.getEntry(term) is not None:
            return True
        return False


    @staticmethod
    def getEntry(id):
        return AST.symbolTable.getTable().get(id)
