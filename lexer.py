import ply.lex as lex
import tokrules

class Lexer:
    def __init__(self, source):
        self.source = source
        # Build the lexer
        self.lexer = lex.lex(module=tokrules)
        self.lexer.input(self.source)

    def getToken(self):
        tok = self.lexer.token()
        if not tok:
            # Add EOF token
            t = lex.LexToken()
            t.type = 'EOF'
            t.value = ''
            return t
        else:
            return tok

    def getAllTokens(self):
        tokens = []
        while True:
            tok = self.getToken()
            tokens.append(tok)
            if tok.type == 'EOF':
                break      # No more input
            # print(tok.type, tok.value, tok.lineno, tok.lexpos)
            # LexToken(IDENTIFIER,'d1',1,0)
            # IDENTIFIER d1 1 0

        return tokens
