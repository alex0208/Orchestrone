import sys
sys.path.append('..')

import unittest
from drone_parser import Parser
from lexer import Lexer
import ply.lex as lex


class TestLexer(unittest.TestCase):

    def test_get_new_token(self):
        lexer = Lexer("new")
        token = lexer.getToken()
        assert type(token) is lex.LexToken
        assert token.type == 'NEW'
        assert token.value == 'new'

    def test_get_drone_token(self):
        lexer = Lexer("Drone")
        token = lexer.getToken()
        assert type(token) is lex.LexToken
        assert token.type == 'DRONE'
        assert token.value == 'Drone'

    def test_get_group_token(self):
        lexer = Lexer("Group")
        token = lexer.getToken()
        assert type(token) is lex.LexToken
        assert token.type == 'GROUP'
        assert token.value == 'Group'

    def test_initialize_drone_tokens(self):
        source = """d1 = new Drone(\"IP\");"""
        lexer = Lexer(source)
        tokens  = lexer.getAllTokens()
        token_types = [t.type for t in tokens]
        token_values = [t.value for t in tokens]
        assert token_types == ['IDENTIFIER', 'ASSIGN', 'NEW', 'DRONE', 'LPAREN', 'STRING', 'RPAREN', 'SEMICOLON', 'EOF']
        assert token_values == ['d1', '=', 'new', 'Drone', '(', '"IP"', ')', ';', '']

    def test_initialize_group(self):
        source = """group = new Group(initial_formation);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        token_types = [t.type for t in tokens]
        token_values = [t.value for t in tokens]
        assert token_types == ['IDENTIFIER', 'ASSIGN', 'NEW', 'GROUP', 'LPAREN', 'IDENTIFIER', 'RPAREN', 'SEMICOLON', 'EOF']
        assert token_values == ['group', '=', 'new', 'Group', '(', 'initial_formation', ')', ';', '']

    def test_initialize_formation(self):
        source = """formation = new Formation([{drone:d1,x:1,y:1}]);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        token_types = [t.type for t in tokens]
        token_values = [t.value for t in tokens]
        assert token_types == ['IDENTIFIER', 'ASSIGN', 'NEW', 'FORMATION', 'LPAREN', 'LBRACK', 'LBLOCK', 'IDENTIFIER',
                               'COLON', 'IDENTIFIER', 'COMA', 'IDENTIFIER', 'COLON', 'NUMBER', 'COMA', 'IDENTIFIER',
                               'COLON', 'NUMBER', 'RBLOCK', 'RBRACK', 'RPAREN', 'SEMICOLON', 'EOF']
        assert token_values == ['formation', '=', 'new', 'Formation', '(', '[', '{', 'drone', ':', 'd1', ',', 'x',
                                ':', 1, ',', 'y', ':', 1, '}', ']', ')', ';', '']

    def test_initialize_transition(self):
        source = """transition = new Transition(formation, 10);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        token_types = [t.type for t in tokens]
        token_values = [t.value for t in tokens]
        assert token_types == ['IDENTIFIER', 'ASSIGN', 'NEW', 'TRANSITION', 'LPAREN', 'IDENTIFIER',
                               'COMA', 'NUMBER', 'RPAREN', 'SEMICOLON', 'EOF']
        assert token_values == ['transition', '=', 'new', 'Transition', '(', 'formation', ',', 10, ')', ';', '']


    def test_assign_number_variable(self):
        source = """height = 10;"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        token_types = [t.type for t in tokens]
        token_values = [t.value for t in tokens]
        assert token_types == ['IDENTIFIER', 'ASSIGN', 'NUMBER', 'SEMICOLON', 'EOF']
        assert token_values == ['height', '=', 10, ';', '']

    def test_arithmetics(self):
        source = """b = 5 + 7 + 4 + 10 + 5 / 2 - 10 * 4;"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        token_types = [t.type for t in tokens]
        token_values = [t.value for t in tokens]
        assert token_types == ['IDENTIFIER', 'ASSIGN', 'NUMBER', 'PLUS', 'NUMBER', 'PLUS', 'NUMBER', 'PLUS', 'NUMBER',
                               'PLUS', 'NUMBER', 'DIVIDE', 'NUMBER', 'MINUS', 'NUMBER', 'TIMES', 'NUMBER',
                               'SEMICOLON', 'EOF']
        assert token_values == ['b', '=', 5, '+', 7, '+', 4, '+', 10, '+', 5, '/', 2, '-', 10, '*', 4, ';', '']

    def test_user_function(self):
        source = """function special_loop(group, transition_list, number_loops)
                    {
                        group.takeOff(5);
                        group.loop(transition_list, number_loops);
                        group.land();
                    }"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        token_types = [t.type for t in tokens]
        token_values = [t.value for t in tokens]
        assert token_types == ['FUNCTION', 'IDENTIFIER', 'LPAREN', 'IDENTIFIER', 'COMA', 'IDENTIFIER',
                               'COMA', 'IDENTIFIER', 'RPAREN', 'LBLOCK','IDENTIFIER', 'DOT', 'IDENTIFIER',
                               'LPAREN', 'NUMBER', 'RPAREN', 'SEMICOLON', 'IDENTIFIER', 'DOT', 'IDENTIFIER',
                               'LPAREN', 'IDENTIFIER', 'COMA', 'IDENTIFIER', 'RPAREN', 'SEMICOLON',
                               'IDENTIFIER', 'DOT', 'IDENTIFIER', 'LPAREN', 'RPAREN', 'SEMICOLON', 'RBLOCK', 'EOF']
        assert token_values == ['function', 'special_loop', '(', 'group', ',', 'transition_list', ',',
                                'number_loops', ')', '{', 'group', '.', 'takeOff', '(', 5, ')', ';',
                                'group', '.', 'loop', '(', 'transition_list', ',', 'number_loops', ')', ';',
                                'group', '.', 'land', '(', ')', ';', '}', '']

    def test_function_call(self):
        source = """special_loop(group, transition_list, number_loops);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        token_types = [t.type for t in tokens]
        token_values = [t.value for t in tokens]
        assert token_types == ['IDENTIFIER', 'LPAREN', 'IDENTIFIER', 'COMA', 'IDENTIFIER',
                               'COMA', 'IDENTIFIER', 'RPAREN', 'SEMICOLON', 'EOF']
        assert token_values == ['special_loop', '(', 'group', ',', 'transition_list', ',',
                                'number_loops', ')', ';', '']

if __name__ == '__main__':
    unittest.main()