#!/usr/bin/python3

import re
import deadCode
import redundantLoads
from itertools import zip_longest
from math import inf

#class Instruction:
#    def __init__(self, type, data):
#        self.type = type
#        self.data = data
#
#        pass

# Returns all objects that are connected to `start`
def connected(start):
    visited = set()
    nodes = [start]
    while len(nodes) > 0:
        node = nodes.pop()
        if node not in visited:
            visited.add(node)
            for e in node.edges:
                nodes.append(e)

    return visited

# Return a tuple relevant to the instruction
def parse_instruction(name, re):
    if name == "lc":
        return ["lc", int(re.group(1)), int(re.group(2))]
    elif name == "ld":
        return ["ld", int(re.group(1)), re.group(2)]
    elif name == "st":
        return ["st", re.group(1), int(re.group(2))]
    elif name == "add":
        return ["add", int(re.group(1)), int(re.group(2)), int(re.group(3))]
    elif name == "sub":
        return ["sub", int(re.group(1)), int(re.group(2)), int(re.group(3))]
    elif name == "mul":
        return ["mul", int(re.group(1)), int(re.group(2)), int(re.group(3))]
    elif name == "div":
        return ["div", int(re.group(1)), int(re.group(2)), int(re.group(3))]
    elif name == "lt":
        return ["lt", int(re.group(1)), int(re.group(2)), int(re.group(3))]
    elif name == "gt":
        return ["gt", int(re.group(1)), int(re.group(2)), int(re.group(3))]
    elif name == "eq":
        return ["eq", int(re.group(1)), int(re.group(2)), int(re.group(3))]
    elif name == "br":
        return ["br", int(re.group(1)), int(re.group(2)), int(re.group(3))]
    elif name == "ret":
        return ["ret", int(re.group(1))]
    elif name == "call":
        return ["call", int(re.group(1)), re.group(2), [int(s[1:]) for s in re.group(3).split(' ')]]
    else:
        return None

# Contains a list of instructions
class CFG_Block:
    def __init__(self, id, parent):
        self.instructions = []  # Instructions this block contains
        self.id = id
        self.parent = parent

        self.edges = set()
        self.in_edges = set()
        self.out_edges = set()

        self.registers = set()

        self.blocks = [] # Other blocks this block branches to

    def __repr__(self):
        return str(self.id) + "@" + str(self.parent)

    def __str__(self):
        operators = ["add", "sub", "mul", "div", "lt", "gt", "eq",]
        sing_regs = ["lc", "ld", "br", "ret", "call",]
        out = " " * 6 + "(" + str(self.id)
        out_instr = []
        for name, *args in self.instructions:
            out_instr.append(" " * 4 + "(" + name + " ")
            if name in operators:
                args = ["r" + str(a) for a in args]
            elif name in sing_regs:
                args[0] = "r" + str(args[0])
            elif name == "st":
                args[1] = "r" + str(args[1])

            if name == "call":
                args[2] = ["r" + str(a) for a in args[2]]
                out_instr[-1] += " ".join(map(str, args[0:2])) + " " + " ".join(args[2])
            else:
                out_instr[-1] += " ".join(map(str, args))

            out_instr[-1] += ")"
        if len(out_instr) > 0:
            out_instr = [out_instr[0]] + [" " * 8 + s for s in out_instr[1:]]
        return out + "\n".join(out_instr) + " )"

    def __eq__(self, other):
        if other is None:
            return False
        if not self.id == other.id:
            return False
#        if not (self.edges == other.edges or
#         self.in_edges == other.in_edges or 
#         self.out_edges == other.out_edges):
#            return False
        for si, oi in zip_longest(self.instructions, other.instructions):
            if si is None:
                return False

            if not si == oi:
                return False
        return True

    def __hash__(self):
        return hash(str(self))

    def clone(self, parent):
        ret = CFG_Block(self.id, parent)
        ret.instructions = [i for i in self.instructions]

        return ret

    def add_instruction(self, instruction):
        if instruction is not None:
            self.instructions.append(instruction)

    def add_edge(self, edge, undirected=True):
        if edge is not None:
            self.edges.add(edge)
            self.out_edges.add(edge)
            edge.in_edges.add(self)
            if undirected and self not in edge.edges:
                edge.edges.add(self)

    def connect(self):
        # Reset the sets
        self.edges = set()

        p = self.parent
        fall_through = True

        for name, *args in self.instructions:
            if name == "call":
                p.add_edge(p.parent.find(args[1]))  # Add an edge to the parent function
            elif name == "br":
                self.add_edge(p.find(args[1]))
                self.add_edge(p.find(args[2]))

            if name == "ret" or name == "br":
                fall_through = False

        # Add the next block if current block does not exit prematurely
        if fall_through and p.blocks.count(self) == 1:
            index = p.blocks.index(self)
            self.add_edge(p.blocks[index + 1] if len(p.block) >= index + 1 else None)

    def unreachable_code(self):
        for i, (name, *args) in enumerate(self.instructions):
            if name == "ret" or name == "br":
                self.instructions = self.instructions[0:i + 1]
                break

# Contains a list of blocks
class CFG_Function:
    def __init__(self, name, arguments, parent):
        self.blocks = []     # Blocks of instructions that this function contains

        self.name = name
        self.args = arguments

        self.edges = set()
        self.in_edges = set()
        self.out_edges = set()

        self.parent = parent

#    def __repr__(self):
#        return self.name + "(" + ", ".join(self.args) + ")"

    def __str__(self):
        out = "(" + self.name + " (" + " ".join(self.args) + ")\n"
        out_blocks = []
        for b in self.blocks:
            out_blocks.append(str(b))
        out += "\n".join(out_blocks) + " )"
        return out

    def __eq__(self, other):
        if other is None:
            return False

        if not self.name == other.name:
            return False

        if not self.args == other.args:
            return False

        for sb, ob in zip_longest(self.blocks, other.blocks):
            if sb is None:
                return False

            if not sb == ob:
                return False

        return True

    def __hash__(self):
        return hash(str(self))

    def clone(self, parent):
        ret = CFG_Function(self.name, self.args, parent)
        for b in self.blocks:
            ret.add_block(b.clone(ret))
        
        return ret

    # Finds a block that matches id `id`, otherwise returns None
    def find(self, id):
        for b in self.blocks:
            if b.id == id:
                return b
        return None

    def add_edge(self, edge, undirected=True):
        if edge is not None:
            self.edges.add(edge)
            self.out_edges.add(edge)
            edge.in_edges.add(self)
            if undirected and self not in edge.edges:
                edge.edges.add(self)

    def add_block(self, block):
        if block is not None:
            self.blocks.append(block)

    def connect(self):
        # Reset the sets
        self.edges = set()

        for b in self.blocks:
            b.connect()

    def unreachable_code(self):
        fblock = self.blocks[0]  # Get the first block in function body (may not be block 0)
        d_blks = set(self.blocks) - connected(fblock)
        self.blocks = [b for b in self.blocks if b not in d_blks]

        for b in self.blocks:
            b.unreachable_code()

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

    def __str__(self):
        out = "("
        out_funcs = []
        for f in self.functions:
            out_funcs.append(str(f))
        out_funcs = [" " * 2 + out_funcs[0]] + [" " * 3 + s for s in out_funcs[1:]]
        out += "\n".join(out_funcs) + " )"
        return out

    def __eq__(self, other):
        for sf, of in zip_longest(self.functions, other.functions):
            if sf is None:
                return False
            if not sf == of:
                return False
        return True

    def clone(self):
        ret = CFG()
        for f in self.functions:
            ret.functions.append(f.clone(ret))

        ret.connect()
        return ret

    # Finds a function with name `name` in program, otherwise returns None
    def find(self, name):
        for f in self.functions:
            if f.name == name:
                return f
        return None

    # Converts the list of strings, ir, into a CFG data structure
    def parse(self, ir):
        function = None  # Current function we're in
        block = None     # Current block we're in
        
        i = 0
        while i < len(ir):
            cf = self.dfun.match(ir[i:])
            if cf is not None:
                function = CFG_Function(cf.group(1), cf.group(2).split(' '), self)
                self.functions.append(function)
                i += len(cf.group(0))

            cb = self.dbr.match(ir[i:])
            if cb is not None:
                block = CFG_Block(int(cb.group(1)), function)
                function.add_block(block)
                i += len(cb.group(0))

            match = None
            for r in self.instrs:
                match = r["re"].match(ir[i:])
                if match is not None:
                    block.add_instruction(parse_instruction(r["name"], match))
                    break

            i += 1

#        for line in ir:
#            # Check if a new function block is defined here
#            cf = self.dfun.search(line)
#            if cf is not None:
#                function = CFG_Function(cf.group(1), cf.group(2).split(' '), self)
#                self.functions.append(function)
#
#            # Check if a new block is defined here
#            cb = self.dbr.search(line)
#            if cb is not None:
#                # Update block
#                block = CFG_Block(int(cb.group(1)), function)
#                function.add_block(block)
#
#            # Parse the instruction
#            match = None
#            for r in self.instrs:
#                match = r["re"].search(line)
#                if match is not None:
#                    block.add_instruction(parse_instruction(r["name"], match))
#                    break

    def connect(self):
        # Reset all program edges
        for f in self.functions:
            f.edges = set()
            f.in_edges = set()
            f.out_edges = set()
            for b in f.blocks:
                b.edges = set()
                b.in_edges = set()
                b.out_edges = set()

        for f in self.functions:
            f.connect()

    def unreachable_code(self):
        main = self.find("main")  # Find the `main' function
        d_funs = set(self.functions) - connected(main)  # Find all functions disconnected from `main'
        self.functions = [f for f in self.functions if f not in d_funs]  # Remove them

        for f in self.functions:
            f.unreachable_code()

# Read an entire file and return a list of strings representing each line
def read_file(filename):
    with open(filename, "r") as f:
        ret = f.read()
#        ret = [l.strip() for l in f.read().splitlines()]
    return ret

if __name__ == "__main__":
    import sys
    import os.path
    import argparse

    arg_parse = argparse.ArgumentParser(prog = "ir_optimise",
                                     description = "Optimises *correct* intermediate representation programs generated by the COMP3109 Assignment 2 compiler. Specifying a file containing invalid IR code will result in undefined behaviour and potential crashes.",
                                     epilog = "Not specifying an optimisation technique or having 0 passes will result in no changes and will output the original program.")
    arg_parse.add_argument("-i", "--input", type = str, help = "Input IR file (required)", required = True)
    arg_parse.add_argument("-o", "--output", type = str, help = "Output IR file (not specifying will print to stdout)")
    arg_parse.add_argument("-u", "--unreachable-code", action = "store_true", help = "Remove unreachable code")
    arg_parse.add_argument("-d", "--dead-code", action = "store_true", help = "Remove dead code")
    arg_parse.add_argument("-r", "--redundant-loads", action = "store_true", help = "Remove redundant load instructions")
    arg_parse.add_argument("-n", "-p", "--passes", type = int, default = -1, help = "Number of optimisation passes to perform. Values < 0 will perform as many passes until no more optimisations can be made (default: -1)")

    args = arg_parse.parse_args()
    # The first argument in Python is the file/program name, so we check for a length of 2
    if args.input is not None:
        if os.path.isfile(args.input):
            in_file = read_file(args.input)
            if len(in_file) != 0:
                prev_cfg = CFG()
                cfg = CFG(in_file)
                if args.passes < 0:
                    npass = -inf
                else:
                    npass = 0

                while npass < args.passes:
                    # No more optimisations possible
                    if prev_cfg == cfg:
                        break

                    prev_cfg = cfg
                    cfg = CFG(str(prev_cfg).replace("\n", " "))
                    cfg.connect()

                    if args.unreachable_code:
                        cfg.unreachable_code()
                    if args.dead_code:
                        deadCode.dce(cfg)
                    if args.redundant_loads:
                        redundantLoads.rle(cfg)

                    npass += 1

                if args.output is not None:
                    f = open(args.output, "w")
                    f.write(str(cfg) + "\n")
                else:
                    print(str(cfg))
        else:
            print("Error: File '" + args.input + "' does not exist.")
