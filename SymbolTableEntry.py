class SymbolTableEntry:
    def __init__(self, identifier, entry_type, value):
        self.identifier = identifier
        self.type = entry_type
        self.value = value

    def getValueFromId(self, id):
        if self.identifier is id:
            print(id)

    def containsId(self, id):
        if self.identifier == id:
            return True
        return False

    def __str__(self):
        return '{:<30} {:^30} {:>30}'.format(self.identifier, self.type, str(self.value))

