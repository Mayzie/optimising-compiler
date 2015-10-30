#!/usr/bin/python3

import re

#class Instruction:
#    def __init__(self, type, data):
#        self.type = type
#        self.data = data
#
#        pass

# Contains a list of instructions
class CFG_Blocks:
    def __init__(self):
        self.instructions = []  # Instructions this block contains

        pass

# Contains a list of blocks
class CFG_Function:
    def __init__(self):
        self.blocks = []     # Blocks of instructions that this function contains
        self.functions = []  # Other functions this function calls

        pass

# Contains a list of functions which link to other functions they call
class CFG:
    instr_lc = re.compile("\(lc\s+r([1-9][0-9]*)\s+([0-9]+)\)")
    instr_ld = re.compile("\(ld\s+r([1-9][0-9]*)\s+([A-z][A-z0-9]*)\)")
    instr_st = re.compile("\(st\s+([A-z][A-z0-9]*)\s+r([1-9][0-9]*)\)")
    instr_add = re.compile("\(add\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")
    instr_sub = re.compile("\(sub\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")
    instr_mul = re.compile("\(mul\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")
    instr_div = re.compile("\(div\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")
    instr_lt = re.compile("\(lt\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")
    instr_gt = re.compile("\(gt\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")
    instr_eq = re.compile("\(eq\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\s+r([1-9][0-9]*)\)")
    instr_br = re.compile("\(br\s+r([1-9][0-9]*)\s+(-?[0-9]+)\s+(-?[0-9]+)\)")
    instr_ret = re.compile("\(ret\s+r([1-9][0-9]+)\)")
    instr_call = re.compile("\(call\s+r([1-9][0-9]+)\s+(-?[0-9]+)\s+((r[1-9][0-9]*)*)\)")

    def __init__(self, ir=None):
        self.functions = []

        if not ir == None:
            self.parse(ir)

    # Converts the list of strings, ir, into a CFG data structure
    def parse(self, ir):
        for line in ir:
            # ToDo: What is here atm is just for testing/design purposes
            match = self.instr_lc.match(line)
            if match is not None:
                print("Instruction: lc. Registers:", match.group(1), match.group(2))
            match = self.instr_ld.match(line)
            if match is not None:
                print("Instruction: ld. Put", match.group(2), "Into register:", match.group(1))
        pass

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
            print(in_file)
            if len(in_file) != 0:
                cfg = CFG(in_file)
        else:
            print("Error: File '" + sys.argv[1] + "' does not exist.")
    else:
        print("Error: Invalid number of arguments. Need exactly 1 argument, the IR filename.")
