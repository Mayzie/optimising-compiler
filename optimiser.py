#!/usr/bin/python3

import re
import deadCode
import redundantLoads

#class Instruction:
#    def __init__(self, type, data):
#        self.type = type
#        self.data = data
#
#        pass

# Return a tuple relevant to the instruction
def parse_instruction(name, re):
    if name == "lc":
        return ("lc", int(re.group(1)), int(re.group(2)))
    elif name == "ld":
        return ("ld", int(re.group(1)), re.group(2))
    elif name == "st":
        return ("st", re.group(1), int(re.group(2)))
    elif name == "add":
        return ("add", int(re.group(1)), int(re.group(2)), int(re.group(3)))
    elif name == "sub":
        return ("sub", int(re.group(1)), int(re.group(2)), int(re.group(3)))
    elif name == "mul":
        return ("mul", int(re.group(1)), int(re.group(2)), int(re.group(3)))
    elif name == "div":
        return ("div", int(re.group(1)), int(re.group(2)), int(re.group(3)))
    elif name == "lt":
        return ("lt", int(re.group(1)), int(re.group(2)), int(re.group(3)))
    elif name == "gt":
        return ("gt", int(re.group(1)), int(re.group(2)), int(re.group(3)))
    elif name == "eq":
        return ("eq", int(re.group(1)), int(re.group(2)), int(re.group(3)))
    elif name == "br":
        return ("br", int(re.group(1)), int(re.group(2)), int(re.group(3)))
    elif name == "ret":
        return ("ret", int(re.group(1)))
    elif name == "call":
        return ("call", int(re.group(1)), re.group(2), [int(s[1:]) for s in re.group(3).split(' ')])
    else:
        return None

# Contains a list of instructions
class CFG_Block:
    def __init__(self, id, parent):
        self.instructions = []  # Instructions this block contains
        self.id = id
        self.parent = parent
        self.edges = set()
        self.blocks = [] # Other blocks this block branches to

    def add_instruction(self, instruction):
        if instruction is not None:
            self.instructions.append(instruction)
        else:
            print("No instruction")

    def add_edge(self, edge, undirected=True):
        if edge is not None:
            self.edges.add(edge)
            if undirected and edge not in self.edges:
                edge.add_edge(self)

    def pretty_print(self):
        for instruction in self.instructions:
            print(instruction)

    def connect(self):
        # Reset the sets
        self.edges = set()

        p = self.parent

        for name, *args in self.instructions:
            if name == "call":
                p.add_edge(p.parent.find(args[1]))  # Add an edge to the parent function
            elif name == "br":
                self.add_edge(p.find(args[1]))
                self.add_edge(p.find(args[2]))
        self.add_edge(p.find(self.id + 1))  # Add next block number

# Contains a list of blocks
class CFG_Function:
    def __init__(self, name, arguments, parent):
        self.blocks = []     # Blocks of instructions that this function contains
        self.functions = []  # Other functions this function calls

        self.name = name
        self.args = arguments
        self.edges = set()

        self.parent = parent

    # Finds a block that matches id `id`, otherwise returns None
    def find(self, id):
        for b in self.blocks:
            if b.id == id:
                return b
        return None

    def add_edge(self, edge, undirected=True):
        if edge is not None:
            self.edges.add(edge)
            if undirected and edge not in self.edges:
                edge.add_edge(self)

    def add_block(self, block):
        if block is not None:
            self.blocks.append(block)

    def pretty_print(self):
        print("(function '" + self.name + "' " + str(self.args) + "")
        for block in self.blocks:
            print("(block " + str(block.id))
            block.pretty_print()

    def connect(self):
        # Reset the sets
        self.edges = set()

        for b in self.blocks:
            b.connect()

# Contains a list of functions which link to other functions they call
class CFG:
    dfun = re.compile("\(([A-z][A-z0-9]*)\s+\(((\s*[A-z][A-z0-9]*\s*)*)\)")
    dbr = re.compile("\((-?[0-9]+)\s+")

    ilc = {"name" : "lc", "re" : re.compile("\(lc\s+r([1-9][0-9]*)\s+([0-9]+)\)")}
    ild = {"name" : "ld", "re" : re.compile("\(ld\s+r([1-9][0-9]*)\s+([A-z][A-z0-9]*)\)")}
    ist = {"name" : "st", "re" : re.compile("\(st\s+([A-z][A-z0-9]*)\s+r([1-9][0-9]*)\)")}
    iadd = {"name" : "add", "re" : re.compile("\(add\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")}
    isub = {"name" : "sub", "re" : re.compile("\(sub\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")}
    imul = {"name" : "mul", "re" : re.compile("\(mul\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")}
    idiv = {"name" : "div", "re" : re.compile("\(div\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")}
    ilt = {"name" : "lt", "re" : re.compile("\(lt\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")}
    igt = {"name" : "gt", "re" : re.compile("\(gt\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")}
    ieq = {"name" : "eq", "re" : re.compile("\(eq\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")}
    ibr = {"name" : "br", "re" : re.compile("\(br\s+r([1-9][0-9]*)\s+(-?[0-9]+)\s+(-?[0-9]+)\)")}
    iret = {"name" : "ret", "re" : re.compile("\(ret\s+r([1-9][0-9]*)\)")}
    icall = {"name" : "call", "re" : re.compile("\(call\s+r([1-9][0-9]*)\s+([A-z][A-z0-9]*)\s+((\s*r[1-9][0-9]*\s*)*)\)")}
    instrs = [ilc, ild, ist, iadd, isub, imul, idiv, ilt, igt, ieq, ibr, iret, icall, ]

    def __init__(self, ir=None):
        self.functions = []

        if ir is not None:
            self.parse(ir)

    # Finds a function with name `name` in program, otherwise returns None
    def find(self, name):
        for f in self.functions:
            if f.name == name:
                return f
        return None

    def pretty_print(self):
        for function in self.functions:
            function.pretty_print()

    # Converts the list of strings, ir, into a CFG data structure
    def parse(self, ir):
        function = None  # Current function we're in
        block = None     # Current block we're in

        for line in ir:
            # Check if a new function block is defined here
            cf = self.dfun.search(line)
            if cf is not None:
                function = CFG_Function(cf.group(1), cf.group(2).split(' '), self)
                self.functions.append(function)

            # Check if a new block is defined here
            cb = self.dbr.search(line)
            if cb is not None:
                # Update block
                block = CFG_Block(int(cb.group(1)), function)
                function.add_block(block)

            # Parse the instruction
            match = None
            for r in self.instrs:
                match = r["re"].search(line)
                if match is not None:
                    block.add_instruction(parse_instruction(r["name"], match))
                    break

    def connect(self):
        # Reset all program edges
        for f in self.functions:
            f.edges = set()
            for b in f.blocks:
                b.edges = set()

        for f in self.functions:
            f.connect()

# Read an entire file and return a list of strings representing each line
def read_file(filename):
    with open(filename, "r") as f:
        ret = [l.strip() for l in f.read().splitlines()]
    return ret

if __name__ == "__main__":
    import sys
    import os.path

    # The first argument in Python is the file/program name, so we check for a length of 2
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            in_file = read_file(sys.argv[1])
            if len(in_file) != 0:
                cfg = CFG(in_file)
                cfg.connect()
                deadCode.dce(cfg)
                #redundantLoads.rle(cfg)
                cfg.prettyPrint()
        else:
            print("Error: File '" + sys.argv[1] + "' does not exist.")
    else:
        print("Error: Invalid number of arguments. Need exactly 1 argument, the IR filename.")
