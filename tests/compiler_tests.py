import sys
sys.path.append('..')

import unittest
from drone_parser import Parser
from lexer import Lexer
from compiler import Compiler
from SymbolTable import SymbolTable
from SymbolTableEntry import SymbolTableEntry
from Command import TakeOffCmd, LoopCmd, LandCmd, WaitCmd, TransitionCmd
from AST import AST

class TestCompiler(unittest.TestCase):

    def test_compiler_init(self):
        source = """d1 = new Drone("ip1");
            d2 = new Drone("ip2");

            initial_formation = new Formation([{drone:d1,x:1,y:1},{drone:d2,x:2,y:1}]);
            group = new Group(initial_formation);

            group.takeOff(10);

            second_formation = new Formation([{drone:d1,x:1,y:2},{drone:d2,x:2,y:2}]);

            transition = new Transition(second_formation, 10);

            group.transition(transition);

            group.wait(5);

            group.land();"""
        AST.symbolTable = SymbolTable()
        AST.instructionsTable = []

        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()



        ast.fillSymbolTable()
        print(ast.instructionsTable)
        compiled = Compiler(ast.instructionsTable)

        assert type(compiled) is Compiler
        assert len(compiled.instructions) == 4
        assert type(compiled.instructions[0]) == TakeOffCmd
        assert type(compiled.instructions[1]) == TransitionCmd
        assert type(compiled.instructions[2]) == WaitCmd
        assert type(compiled.instructions[3]) == LandCmd
        assert len(compiled.start_config) == 2
        assert 'd1' in compiled.start_config
        assert 'd2' in compiled.start_config
        assert len(compiled.udp_commands) == 2
        # FIRST DONE
        # ASCII code for "takeoff"
        assert compiled.udp_commands[0][0] == ['74', '61', '6b', '65', '6f', '66', '66']
        # ASCII code for "back 100"
        assert compiled.udp_commands[0][1] == ['62', '61', '63', '6b', '20', '31', '30', '30']
        # ASCII code for "command" aka the wait command
        assert compiled.udp_commands[0][2] == ['63', '6f', '6d', '6d', '61', '6e', '64']
        # ASCII code for "land"
        assert compiled.udp_commands[0][3] == ['6c', '61', '6e', '64']
        # SECOND DRONE
        # ASCII code for "takeoff"
        assert compiled.udp_commands[1][0] == ['74', '61', '6b', '65', '6f', '66', '66']
        # ASCII code for "back 100"
        assert compiled.udp_commands[1][1] == ['62', '61', '63', '6b', '20', '31', '30', '30']
        # ASCII code for "command" aka the wait command
        assert compiled.udp_commands[1][2] == ['63', '6f', '6d', '6d', '61', '6e', '64']
        # ASCII code for "land"
        assert compiled.udp_commands[1][3] == ['6c', '61', '6e', '64']

    def test_number_assignment_in_symbol_table(self):
        source = """x = 1;"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        symTable = ast.fillSymbolTable()
        table_items = symTable.getTable()

        assert 'x' in table_items
        assert type(table_items['x']) == SymbolTableEntry
        assert table_items['x'].identifier == 'x'
        assert table_items['x'].type == 'NUMBER'
        assert table_items['x'].value == 1

    def test_string_assignment_in_symbol_table(self):
        source = """x = "hello world";"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        symTable = ast.fillSymbolTable()
        table_items = symTable.getTable()

        assert 'x' in table_items
        assert type(table_items['x']) == SymbolTableEntry
        assert table_items['x'].identifier == 'x'
        assert table_items['x'].type == 'STRING'
        assert table_items['x'].value == '"hello world"'

    def test_drone_assignment_in_symbol_table(self):
        source = """d1 = new Drone("ip");"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        symTable = ast.fillSymbolTable()
        table_items = symTable.getTable()


        assert 'd1' in symTable.getTable()
        assert type(table_items['d1']) == SymbolTableEntry
        assert table_items['d1'].identifier == 'd1'
        assert table_items['d1'].type == 'Drone'
        assert table_items['d1'].value == '"ip"'


    def test_formation_assignment_in_symbol_table(self):
        source = """formation = new Formation([{drone:d1,x:0,y:0}]);"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        symTable = ast.fillSymbolTable()
        table_items = symTable.getTable()

        assert 'formation' in table_items
        assert type(table_items['formation']) == SymbolTableEntry
        assert table_items['formation'].identifier == 'formation'
        assert table_items['formation'].type == 'Formation'
        assert table_items['formation'].value == [('d1', 0, 0)]

    def test_group_assignment_in_symbol_table(self):
        source = """formation = new Formation([{drone:d1,x:0,y:0}]);
                    group = new Group(formation);"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        symTable = ast.fillSymbolTable()
        table_items = symTable.getTable()

        assert 'formation' in table_items
        assert 'group' in table_items
        # assert type(table_items['group']) == SymbolTableEntry
        for key, value in symTable.getTable().items():
            assert type(key) is str
            assert type(value) is SymbolTableEntry
        assert table_items['group'].identifier == 'group'
        assert table_items['group'].type == 'Group'
        assert table_items['group'].value == [('d1', 0, 0)]

    def test_transition_assignment_in_symbol_table(self):
        source = """formation = new Formation([{drone:d1,x:0,y:0}]);
        transition = new Transition(formation, 10);"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        symTable = ast.fillSymbolTable()
        table_items = symTable.getTable()

        assert 'formation' in table_items
        assert 'transition' in table_items

        for key, value in symTable.getTable().items():
            assert type(key) is str
            assert type(value) is SymbolTableEntry

        assert table_items['transition'].identifier == 'transition'
        assert table_items['transition'].type == 'Transition'
        assert table_items['transition'].value == [('d1',0,0)]

    def test_function_declaration_in_symbol_table(self):
        source = """function special_loop(group, transition_list, number_loops)
                {
                    group.takeOff(5);
                    group.loop(transition_list, number_loops);
                    group.land();
                }"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        symTable = ast.fillSymbolTable()
        table_items = symTable.getTable()

        assert 'special_loop' in table_items

        for key, value in symTable.getTable().items():
            assert type(key) is str
            assert type(value) is SymbolTableEntry

        assert table_items['special_loop'].identifier == 'special_loop'
        assert table_items['special_loop'].type == 'FUNCTION'
        assert type(table_items['special_loop'].value) == dict
        assert len(table_items['special_loop'].value['args']) == 3
        assert table_items['special_loop'].value['args'] == ['group', 'transition_list', 'number_loops']
        assert len(table_items['special_loop'].value['asssignments']) == 3
        assert type(table_items['special_loop'].value['asssignments'][0].cmd) == TakeOffCmd
        assert type(table_items['special_loop'].value['asssignments'][1].cmd) == LoopCmd
        assert type(table_items['special_loop'].value['asssignments'][2].cmd) == LandCmd

    def test_wrong_group_assignment_raises_error(self):
        source = """group = new Group(formation);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()

        #Program.Assignment.Expression.Group.Formation.fillSymbolTable
        self.assertRaises(Exception, ast.assignments[0].expr.obj.formation.fillSymbolTable())
        # self.assertRaises(Exception, ast.fillSymbolTable)

    def test_compiler_fail_only_assignments(self):
        source = """x = 10;"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        symTable = ast.fillSymbolTable()

        self.assertRaises(Exception, Compiler)



    def test_compiler_no_transition(self):
        source = """d1 = new Drone("ip1");
                    d2 = new Drone("ip2");

                    initial_formation = new Formation([{drone:d1,x:1,y:1},{drone:d2,x:2,y:1}]);
                    group = new Group(initial_formation);

                    group.takeOff(10);

                    second_formation = new Formation([{drone:d1,x:1,y:2},{drone:d2,x:2,y:2}]);

                    group.wait(5);

                    group.land();"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        ast.symbolTable = SymbolTable()
        ast.fillSymbolTable()
        # Compiler(ast.instructionsTable)
        self.assertRaises(Exception, Compiler)
        # compiled = Compiler(ast.instructionsTable)

    def test_compiler_collisions(self):
        source = """d1 = new Drone("ip1");
                    d2 = new Drone("ip2");

                    initial_formation = new Formation([{drone:d1,x:1,y:1},{drone:d2,x:2,y:1}]);
                    group = new Group(initial_formation);

                    group.takeOff(10);

                    second_formation = new Formation([{drone:d1,x:2,y:1},{drone:d2,x:2,y:2}]);

                    group.wait(5);

                    group.land();"""
        AST.symbolTable = SymbolTable()
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)
        ast = parser.Program()
        ast.symbolTable = SymbolTable()
        ast.fillSymbolTable()
        # Compiler(ast.instructionsTable)
        self.assertRaises(Exception, Compiler)
        # compiled = Compiler(ast.instructionsTable)


if __name__ == "__main__":
    unittest.main()
