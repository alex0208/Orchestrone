from AST import AST

class Command(AST):
    def __init__(self, cmd):
        self.type = cmd

    def prettyprint(self):
        pass

    def fillSymbolTable(self):
        # print(self)
        pass

    def generateInstruction(self):
        pass
    def typeChecking(self):
        pass



class TakeOffCmd(Command):
    def __init__(self, height):
        self.type = "takeOff"
        self.height = height

    def prettyprint(self):
        print("takeOff({})".format(self.height), end="")
        pass

    def generateInstruction(self):
        if isinstance(self.height, str):
            self.height = AST.getEntry(self.height).value
        AST.instructionsTable.append(self)

    def typeChecking(self):
        pass

    def __str__(self):
        return "" + self.type + " " + str(self.height)


class LoopCmd(Command):
    def __init__(self, transition_list, num_loops):
        self.type = "loop"
        self.transition_list = transition_list
        self.num_loops = num_loops

    def prettyprint(self):
        print("loop({},{})".format(self.transition_list, self.num_loops), end="")
        pass

    def generateInstruction(self):
        pass


    def typeChecking(self):
        pass


class LandCmd(Command):
    def __init__(self):
        self.type = "land"

    def prettyprint(self):
        print("land()", end="")
        pass

    def generateInstruction(self):
        AST.instructionsTable.append(self)

    def typeChecking(self):
        pass

    def __str__(self):
        return "Landing"

class TransitionCmd(Command):
    def __init__(self, transition):
        self.type = "transition"
        self.transition = transition

    def prettyprint(self):
        print("transition(", end="")
        self.transition.prettyprint()
        print(")", end="")

    def generateInstruction(self):
        if self.transition.var is not None:
            self.transition = AST.getEntry(self.transition.var).value
        AST.instructionsTable.append(self)

    def typeChecking(self):
        pass

    def __str__(self):
        return "Transition to " + str(self.transition)


class WaitCmd(Command):
    def __init__(self, wait_time):
        self.type = "wait"
        self.wait_time = wait_time

    def prettyprint(self):
        print("wait({})".format(self.wait_time), end="")
        pass

    def generateInstruction(self):
        AST.instructionsTable.append(self)

    def typeChecking(self):
        pass

    def __str__(self):
        return "Waiting " + str(self.wait_time)
