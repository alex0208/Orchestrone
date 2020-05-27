from AST import AST
from Command import Command

class FunctionCall(AST):
    def __init__(self, id, args):
        self.id = id
        self.args = args

    def prettyprint(self):
        print("{}({})".format(self.id, ", ".join(self.args)), end="")

    def fillSymbolTable(self):
        func = AST.getEntry(self.id).value

        if len(self.args) != len(func['args']):
            raise Exception("Function {0} expected {1} arguments but received {2}.".format(self.id, len(func['args']), len(self.args)))

        # Resolve params
        resolved_args = list(map(lambda x: AST.getEntry(x) if isinstance(x, str) else x, self.args))
        resolved_args_dict = dict(zip(func['args'], resolved_args))
        func_sym_table = []


        # when parsing function call it keeps the params from the previous call
        for assign in func['asssignments']:
            if assign.expr:
                func_sym_table.append(assign.expr.fillSymbolTable())
            if assign.cmd:
                if resolved_args_dict.get(assign.id) is None:
                    raise Exception("Variable {} not found.".format(assign.id))
                if resolved_args_dict.get(assign.id).type != 'Group':
                    raise Exception('Expected variable type Group but got {}'.format(resolved_args_dict.get(assign.id).type))
                if assign.cmd.type == 'takeOff':
                    if isinstance(assign.cmd.height, str):
                        tmp_height = resolved_args_dict.get(assign.cmd.height)
                        if tmp_height is None:
                            assign.cmd.height = resolved_args_dict.get(assign.cmd.height).value
                        else: assign.cmd.height = tmp_height
                assign.cmd.generateInstruction()


    def typeChecking(self):
        pass