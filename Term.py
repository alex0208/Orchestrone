from AST import AST

class Term(AST):
    def __init__(self, type=None, term=None, list_terms=None):
        self.type = type
        self.term = term
        self.list_terms = list_terms

    def prettyprint(self):
        if self.list_terms:
            print("[", ", ".join(self.list_terms), "]", end="")
        else:
            print(self.term, end="")

    def fillSymbolTable(self):
        if self.term:
            return self.term
        elif self.list_terms:
            temp_list = []
            for term in self.list_terms:
                temp_list.append(AST.getEntry(term).value)
            return temp_list

    def typeChecking(self):
        pass
