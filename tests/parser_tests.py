import sys
sys.path.append('..')

import unittest
from drone_parser import Parser
from lexer import Lexer
from Drone import Drone
from Expression import Expression
from Term import Term
from Calc import Calc
from Group import Group
from Formation import Formation
from DroneObj import DroneObj
from Command import Command, TakeOffCmd, LoopCmd, TransitionCmd, WaitCmd, LandCmd
from Transition import Transition
from Function import Function
from FunctionCall import FunctionCall


class TestDrone(unittest.TestCase):

    def test_initialize_one_drone(self):
        source = """d1 = new Drone("ip address");"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'd1'
        assert type(result.assignments[0].expr) == Expression
        assert type(result.assignments[0].expr.obj) == Drone
        assert result.assignments[0].expr.obj.ip == '"ip address"'
        assert result.functions == []

    def test_initialize_three_drones(self):
        source = """d1 = new Drone("ip1");
                    d2 = new Drone("ip2");
                    d3 = new Drone("ip3");"""

        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 3
        assert result.assignments[0].id == 'd1'
        assert result.assignments[1].id == 'd2'
        assert result.assignments[2].id == 'd3'
        for asg in result.assignments:
            assert type(asg.expr) == Expression
            assert type(asg.expr.obj) == Drone
        assert result.assignments[0].expr.obj.ip == '"ip1"'
        assert result.assignments[1].expr.obj.ip == '"ip2"'
        assert result.assignments[2].expr.obj.ip == '"ip3"'
        assert result.functions == []

    def test_initialize_group(self):
        source = """group = new Group(initial_formation);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'group'
        assert type(result.assignments[0].expr) == Expression
        assert type(result.assignments[0].expr.obj) == Group
        assert result.assignments[0].expr.obj.formation.var == 'initial_formation'
        assert result.functions == []

    def test_initialize_formation(self):
        source = """formation = new Formation([{drone:d1,x:1,y:1}]);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'formation'
        assert type(result.assignments[0].expr) == Expression
        assert type(result.assignments[0].expr.obj) == Formation
        assert len(result.assignments[0].expr.obj.drones_list) == 1
        assert result.assignments[0].expr.obj.drones_list[0].id == 'd1'
        assert result.assignments[0].expr.obj.drones_list[0].x == 1
        assert result.assignments[0].expr.obj.drones_list[0].y == 1
        assert result.functions == []

    def test_initialize_transition(self):
        source = """transition = new Transition(formation, 5);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'transition'
        assert type(result.assignments[0].expr) == Expression
        assert type(result.assignments[0].expr.obj) == Transition
        assert type(result.assignments[0].expr.obj.formation) == Formation
        assert result.assignments[0].expr.obj.time == 5
        assert result.functions == []

    def test_initialize_wrong_type(self):
        source = """transition = new Type(formation, 5, y);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

    def test_wrong_assignment(self):
        source = """Transition;"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

    def test_wrong_expression(self):
        source = """ x = ; """
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

    def test_initialize_drone_with_wrong_argument_type(self):
        source = """ d1 = new Drone(5); """
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

    def test_initialize_formation_with_wrong_syntax(self):
        source = """ formation = new Formation([{drone:d1,y:1,x:1}]); """
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

        source = """ formation = new Formation([{drone:d1,x:1,z:1}]); """
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

        source = """ formation = new Formation([{y:1,drone:d1,x:1}]); """
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

        source = """ formation = new Formation{[{drone:d1,y:1,x:1}]}; """
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

    def test_initialize_transition_with_wrong_syntax(self):
        source = """ transition = new Transition; """
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        self.assertRaises(Exception, parser.Program)

    def test_assign_number(self):
        source = """height = 5;"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'height'
        assert type(result.assignments[0].expr) == Expression
        assert result.assignments[0].expr.obj == None
        assert type(result.assignments[0].expr.term) == Term
        assert result.assignments[0].expr.term.type == 'NUMBER'
        assert result.assignments[0].expr.term.term == 5
        assert result.functions == []

    def test_assign_string(self):
        source = """str = "hello world";"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'str'
        assert type(result.assignments[0].expr) == Expression
        assert result.assignments[0].expr.obj == None
        assert type(result.assignments[0].expr.term) == Term
        assert result.assignments[0].expr.term.type == 'STRING'
        assert result.assignments[0].expr.term.term == '"hello world"'
        assert result.functions == []

    def test_initialize_list(self):
        source = """list = [5, 6];"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'list'
        assert type(result.assignments[0].expr) == Expression
        assert result.assignments[0].expr.obj == None
        assert type(result.assignments[0].expr.term) == Term
        assert len(result.assignments[0].expr.term.list_terms) == 2
        assert result.assignments[0].expr.term.list_terms[0] == 5
        assert result.assignments[0].expr.term.list_terms[1] == 6
        assert result.functions == []

    def test_arithmetics(self):
        source = """b = 5 + 7 + 4 + 10 + 5 / 2 - 10 * 4;"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'b'
        assert type(result.assignments[0].expr) == Expression
        assert result.assignments[0].expr.obj == None
        assert type(result.assignments[0].expr.term) == Calc
        assert len(result.assignments[0].expr.term.operands) == 8
        assert len(result.assignments[0].expr.term.operators) == 7
        assert result.functions == []

    def test_group_takeOff_method(self):
        source = """group.takeOff(5);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'group'
        assert result.assignments[0].expr == None
        assert type(result.assignments[0].cmd) == TakeOffCmd
        assert result.assignments[0].cmd.height == 5
        assert result.assignments[0].cmd.type == 'takeOff'
        assert result.functions == []

    def test_group_wait_method(self):
        source = """group.wait(5);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'group'
        assert result.assignments[0].expr == None
        assert type(result.assignments[0].cmd) == WaitCmd
        assert result.assignments[0].cmd.wait_time == 5
        assert result.assignments[0].cmd.type == 'wait'
        assert result.functions == []

    def test_group_land_method(self):
        source = """group.land();"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'group'
        assert result.assignments[0].expr == None
        assert type(result.assignments[0].cmd) == LandCmd
        assert result.assignments[0].cmd.type == 'land'
        assert result.functions == []

    def test_group_loop_method(self):
        source = """group.loop(transition_list, 3);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'group'
        assert result.assignments[0].expr == None
        assert type(result.assignments[0].cmd) == LoopCmd
        assert result.assignments[0].cmd.type == 'loop'
        assert result.assignments[0].cmd.num_loops == 3
        assert result.assignments[0].cmd.transition_list == 'transition_list'
        assert result.functions == []

    def test_group_transition_method(self):
        source = """group.transition(transition);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert result.assignments[0].id == 'group'
        assert result.assignments[0].expr == None
        assert type(result.assignments[0].cmd) == TransitionCmd
        assert type(result.assignments[0].cmd.transition) == Transition
        assert result.assignments[0].cmd.type == 'transition'
        assert result.assignments[0].cmd.transition.var == 'transition'
        assert result.functions == []

    def test_write_user_function(self):
        source = """function special_loop(group, transition_list, number_loops)
                    {
                        group.takeOff(5);
                        group.loop(transition_list, number_loops);
                        group.land();
                    }"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 0
        assert len(result.functions) == 1
        assert type(result.functions[0]) == Function
        assert len(result.functions[0].args) == 3
        assert result.functions[0].args[0] == 'group'
        assert result.functions[0].args[1] == 'transition_list'
        assert result.functions[0].args[2] == 'number_loops'
        assert len(result.functions[0].assignments) == 3

    def test_function_call(self):
        source = """function special_loop(group, transition_list, number_loops)
                    {
                        group.takeOff(5);
                        group.loop(transition_list, number_loops);
                        group.land();
                    }


                    special_loop(group, transition_list, number_loops);"""
        lexer = Lexer(source)
        tokens = lexer.getAllTokens()
        parser = Parser(source, tokens)

        assert len(parser.tokens) == len(tokens)

        result = parser.Program()

        assert result is not None
        assert len(result.assignments) == 1
        assert len(result.functions) == 1
        assert type(result.functions[0]) == Function
        assert type(result.assignments[0]) == FunctionCall
        assert result.assignments[0].id == 'special_loop'
        assert len(result.assignments[0].args) == 3
        assert result.assignments[0].args[0] == 'group'
        assert result.assignments[0].args[1] == 'transition_list'
        assert result.assignments[0].args[2] == 'number_loops'


if __name__ == '__main__':
    unittest.main()