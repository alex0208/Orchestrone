# module: tokrules.py
# This module just contains the lexing rules

reserved = (
    'new',
    'Drone',
    'Group',
    'Formation',
    'Transition',
    'function'
)

tokens = tuple(map(lambda s: s.upper(), reserved)) + (
    'NUMBER',
    'LPAREN',  # ()
    'RPAREN',
    'LBRACK',  # []
    'RBRACK',
    'LBLOCK',  # {}
    'RBLOCK',
    'ASSIGN',
    'COMA',
    'COLON',
    'SEMICOLON',
    'DOT',
    'STRING',
    'IDENTIFIER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE'
)

# Regular expression rules for simple tokens
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBLOCK = r'\{'
t_RBLOCK = r'\}'
t_COMA = r'\,'
t_COLON = r'\:'
t_DOT = r'\.'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_STRING = r'\"([^\\\n]|(\\(.|\n)))*?\"'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = t.value.upper()
    return t

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
