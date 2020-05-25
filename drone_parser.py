from Program import Program
from Assignment import Assignment
from Command import Command, TakeOffCmd, LoopCmd, LandCmd, TransitionCmd, WaitCmd
from Transition import Transition
from Formation import Formation
from Group import Group
from Drone import Drone
from Expression import Expression
from Term import Term
from DroneObj import DroneObj
from Calc import Calc
from Function import Function
from FunctionCall import FunctionCall


class Parser:
    def __init__(self, source, tokens):
        # The raw source code
        self.source = source
        # Tokens list of type LexToken
        self.tokens = tokens
        self.last_removed = None
        self.ast = None
        self.debug = False

    def info(self, *msg):
        if self.debug:
            print(*msg)

    def find_column(self, token):
        line_start = self.source.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def peek(self):
        return self.tokens[0]

    def advance(self):
        self.last_removed = self.tokens.pop(0)
        return self.last_removed

    def expect(self, token_type):
        prev = self.last_removed
        tok = self.advance()
        if tok.type != token_type:
            col = self.find_column(prev)
            col = col + len(str(prev.value))
            raise Exception("Expected type {} on line {}, column {} but got {} {}"
                            .format(token_type, prev.lineno, col, tok.type, tok.value))

    def Program(self):
        functions=[]
        if self.peek().type == "FUNCTION":
            functions = self.Functions()

        aslist = self.Assignments()
        return Program(assignments=aslist, functions=functions)

    def Functions(self):
        funlist = []
        while self.peek().type == "FUNCTION":
            fun = self.Function()
            funlist.append(fun)
        return funlist

    def Function(self):
        self.expect("FUNCTION")
        id = self.Identifier()
        self.expect("LPAREN")
        # Parse a list of vars
        args = self.List()
        self.expect("RPAREN")

        self.expect("LBLOCK")
        assignments = self.Assignments()
        self.expect("RBLOCK")
        self.info("Parsed function {} with args {}".format(id, args))
        return Function(id, args, assignments)

    def Assignments(self):
        aslist = []
        tokens = ["EOF", "RBLOCK"]
        while (self.peek().type not in tokens):
            asgn = self.Assignment()
            self.expect("SEMICOLON")
            aslist.append(asgn)
        return aslist

    def Assignment(self):
        id = self.Identifier()
        if self.peek().type == "DOT":
            self.expect("DOT")
            cmd = self.Command()
            # Create new Assign instance and return it
            return Assignment(id, cmd=cmd)
        elif self.peek().type == "ASSIGN":
            self.expect("ASSIGN")
            expr = self.Expression()
            # Create new Assign instance and return it
            return Assignment(id, expr=expr)
        elif self.peek().type == "LPAREN":
            self.expect("LPAREN")
            args = self.List()
            self.expect("RPAREN")
            return FunctionCall(id, args)
        else:
            raise Exception("Expected command or assignment")

    def Identifier(self):
        tok = self.advance()
        # self.info("Parsed identifier:", tok.value)
        return tok.value

    def Command(self):
        cmd = self.advance().value
        if cmd == "takeOff":
            self.expect("LPAREN")
            height = self.advance().value
            self.expect("RPAREN")
            self.info("Parsed takeoff command with height", height)
            return TakeOffCmd(height)
        elif cmd == "loop":
            self.expect("LPAREN")
            transition_list = self.advance().value
            self.expect("COMA")
            num_loops = self.advance().value
            self.expect("RPAREN")
            self.info("Parsed loop command with transition list",
                      "{} and number of loops {}".format(transition_list, num_loops))
            return LoopCmd(transition_list, num_loops)
        elif cmd == "land":
            self.expect("LPAREN")
            self.expect("RPAREN")
            self.info("Parsed command land")
            return LandCmd()
        elif cmd == "transition":
            self.expect("LPAREN")
            trans = self.Transition()
            self.expect("RPAREN")
            self.info("Parsed command transition")
            return TransitionCmd(trans)
        elif cmd == "wait":
            self.expect("LPAREN")
            wait_time = self.advance().value
            self.expect("RPAREN")
            self.info("Parsed wait command with wait time", wait_time)
            return WaitCmd(wait_time)

    def Expression(self):
        tok = self.peek().type
        if tok == "NEW":
            self.expect("NEW")
            obj = self.Type()
            return Expression(obj=obj)
        elif (tok == "NUMBER" or tok == "IDENTIFIER"):
            term = self.Calc()
            return Expression(term=term)
        elif tok == "STRING" or tok == "LBRACK":
            term = self.Term()
            return Expression(term=term)
        else:
            raise Exception("Expected a Type or Term but got", tok)

    def Type(self):
        tok = self.peek().type
        if tok == "DRONE":
            self.expect("DRONE")
            return self.Drone()
        elif tok == "GROUP":
            self.expect("GROUP")
            return self.Group()
        elif tok == "FORMATION":
            self.expect("FORMATION")
            return self.Formation()
        elif tok == "TRANSITION":
            self.expect("TRANSITION")
            return self.Transition()
        else:
            raise Exception("Expected a drone, group, formation or transition",
                            "but got", tok)

    def Drone(self):
        self.expect("LPAREN")
        tok = self.advance()
        if tok.type != "STRING":
            raise Exception("Expected a string IP declaration",
                            "for drone but got", tok.type)

        ip = tok.value
        self.expect("RPAREN")
        self.info("Parsed a new Drone with IP", ip)
        return Drone(ip)

    def Drone_obj(self):
        # {drone:d1,x:1,y:1}
        self.expect("LBLOCK")
        if self.peek().value == "drone":
            # Parse drone argument
            self.advance()
            self.expect("COLON")
            drone = self.advance().value

            self.expect("COMA")

            # Parse x argument
            xt = self.advance()
            if xt.value != "x":
                raise Exception("Drone argument must be followed by x")
            else:
                self.expect("COLON")
                x = self.advance().value

            self.expect("COMA")

            # Parse y argument
            yt = self.advance()
            if yt.value != "y":
                raise Exception("x argument must be followed by y")
            else:
                self.expect("COLON")
                y = self.advance().value

            self.expect("RBLOCK")
            self.info("Parsed drone obj definition of {} x: {}, y: {}"
                      .format(drone, x, y))
            return DroneObj(drone, x, y)
        else:
            raise Exception("Drone obj definition must strat with 'drone'")

    def Drone_list(self):
        drones = []
        self.info("Parsing a drone list")
        while self.peek().type != "RBRACK":
            if self.peek().type == "COMA":
                self.expect("COMA")
            else:
                drones.append(self.Drone_obj())
        return drones

    def Group(self):
        self.expect("LPAREN")
        formation = self.Formation()
        self.expect("RPAREN")
        self.info("Parsed a new Group definition")
        return Group(formation)

    def Formation(self):
        if self.peek().type == "IDENTIFIER":
            t = self.advance()
            self.info("Parsed Formation variable", t.value)
            return Formation(var=t.value)
        elif self.peek().type == "LPAREN":
            # Parse a Formation
            self.expect("LPAREN")

            # Parse list of drone definitions
            self.expect("LBRACK")
            drones_list = self.Drone_list()
            self.expect("RBRACK")

            self.expect("RPAREN")
            return Formation(drones_list=drones_list)
        else:
            raise Exception(
                "Bad Formation declaration, got type: {}".format(self.peek().type))

    def Transition(self):
        if self.peek().type == "IDENTIFIER":
            t = self.advance()
            self.info("Parsed Transition variable", t.value)
            return Transition(var=t.value)
        elif self.peek().type == "LPAREN":
            self.expect("LPAREN")
            form = self.Formation()
            self.expect("COMA")
            time = self.advance().value
            self.expect("RPAREN")
            return Transition(formation=form, time=time)
        else:
            raise Exception("Incorrect transition declaration")

    def Term(self):
        if self.peek().type == "LBRACK":
            self.expect("LBRACK")
            # Parse a list of identifiers
            list_terms = self.List()
            self.expect("RBRACK")
            return Term(list_terms=list_terms)
        else:
            t = self.advance()
            self.info("Parsed a term of type {} and value {}"
                      .format(t.type, t.value))
            return Term(type=t.type, term=t.value)

    def List(self):
        terms = []
        tokens = ["RBRACK", "RPAREN"]
        while (self.peek().type not in tokens):
            if self.peek().type == "COMA":
                # Separator for list items
                self.expect("COMA")
            else:
                t = self.advance()
                self.info("Parsed a list item of type {} and value {}"
                          .format(t.type, t.value))
                terms.append(t.value)
        return terms

    def Calc(self):
        symbols = ["PLUS", "MINUS", "TIMES", "DIVIDE"]
        o1 = self.advance()
        if (self.peek().type in symbols):
            operands = []
            operators = []
            operands.append(o1)
            while (self.peek().type in symbols):
                operator = self.advance()
                o2 = self.advance()
                operands.append(o2)
                operators.append(operator)
            return Calc(operands=operands, operators=operators)
        else:
            return Term(type=o1.type, term=o1.value)
