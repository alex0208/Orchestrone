from copy import deepcopy

from AST import AST
from Command import Command

class FunctionCall(AST):
    def __init__(self, id, args):
        self.id = id
        self.args = args

    def prettyprint(self):
        print("{}({})".format(self.id, ", ".join(self.args)), end="")

    def fillSymbolTable(self):
        func = deepcopy(AST.getEntry(self.id).value)

        if len(self.args) != len(func['args']):
            raise Exception("Function {0} expected {1} arguments but received {2}.".format(self.id, len(func['args']), len(self.args)))

        # Check if variables have been declared
        for arg in self.args:
            if AST.getEntry(arg) == None:
                raise Exception("Variable {}, used in function call {} not defined!".format(arg, self.id))

        # Resolve params
        resolved_args = list(map(lambda x: AST.getEntry(x) if isinstance(x, str) else x, self.args))
        # Map argument names to their real names in the global scope
        resolved_args_dict = dict(zip(func['args'], resolved_args))
        # Symbol table for local scope
        func_sym_table = []


        # when parsing function call it keeps the params from the previous call
        for assign in func['asssignments']:
            if assign.expr:
                func_sym_table.append(assign.expr.fillSymbolTable())
            if assign.cmd:
                
                if resolved_args_dict.get(assign.id) is None:
                    raise Exception("Variable {} not found.".format(assign.id))
                if resolved_args_dict.get(assign.id).type != 'Group':
                    raise Exception('Group command cannot be executed on a non-group variable. Wrong variable: {} {}'
                        .format(resolved_args_dict.get(assign.id).identifier, resolved_args_dict.get(assign.id).type))

                if assign.cmd.type == 'takeOff':
                    tmp_height = resolved_args_dict.get(assign.cmd.height)
                    if isinstance(tmp_height, int):
                        # Assign the height
                        assign.cmd.height = tmp_height.value
                    else:
                        if tmp_height.type != 'NUMBER':
                            raise Exception('The group command takeOff accepts only number types! Provided: {} of type {}'
                                .format(tmp_height.identifier, tmp_height.type))
                        else:
                            # Assign the height
                            assign.cmd.height = tmp_height.value

                elif assign.cmd.type == 'wait':
                    entry = resolved_args_dict.get(assign.cmd.wait_time)
                    if isinstance(entry, int):
                        # Assign the waiting time
                        assign.cmd.wait_time = entry.value
                    else:
                        if entry.type != 'NUMBER':
                            raise Exception('The group command wait accepts only number types! Provided: {} of type {}'
                                .format(entry.identifier, entry.type))
                        else:
                            # Assign the waiting time
                            assign.cmd.wait_time = entry.value

                elif assign.cmd.type == 'transition':
                    entry = resolved_args_dict.get(assign.cmd.transition.var)
                    if entry.type != 'Transition':
                        raise Exception('Transition command accepts only transition types! Provided: {} of type {}'
                            .format(entry.identifier, entry.type))
                    else:
                        # Only set the identifier
                        assign.cmd.transition.var = entry.identifier

                elif assign.cmd.type == 'loop':
                    loops_entry = resolved_args_dict.get(assign.cmd.num_loops)
                    if isinstance(loops_entry, int):
                        # Get the number value
                        assign.cmd.num_loops = entry.value
                    else:
                        if loops_entry.type != 'NUMBER':
                            raise Exception('The loop command accepts only number types for loops! Provided: {} of type {}'
                                .format(loops_entry.identifier, loops_entry.type))
                        else:
                            # Get the number value
                            assign.cmd.num_loops = loops_entry.value

                    transitions_entry = resolved_args_dict.get(assign.cmd.transition_list)
                    if transitions_entry.type != 'LIST':
                        raise Exception('The loop command wait accepts only lists of transitions! Provided: {} of type {}'
                            .format(transitions_entry.identifier, transitions_entry.type))
                    else:
                        # Assign the transition list
                        assign.cmd.transition_list = transitions_entry.value

                assign.cmd.generateInstruction()


    def typeChecking(self):
        pass