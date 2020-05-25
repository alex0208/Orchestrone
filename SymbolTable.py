import SymbolTableEntry

class SymbolTable(object):
    def __init__(self):
        self.__symbol_table = {}

    def addToSymbolTable(self, entry: SymbolTableEntry):
        self.__symbol_table[entry.identifier] = entry

    def getTable(self):
        return self.__symbol_table
