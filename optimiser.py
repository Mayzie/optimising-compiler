#!/usr/bin/python3

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
    def __init__(self, ir=None):
        self.functions = []

        if not ir == None:
            self.parse(ir)

    # Converts the list of strings, ir, into a CFG data structure
    def parse(self, ir):
        pass

# Read an entire file and return a list of strings representing each line
def read_file(filename):
    with open(filename, "r") as f:
        ret = f.read().replace("\n", "")
    return ret

if __name__ == "__main__":
    import sys
    import os.path

    # The first argument in Python is the file/program name, so we check for a length of 2
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            in_file = read_file(sys.argv[1])
        else:
            print("Error: File '" + sys.argv[1] + "' does not exist.")
    else:
        print("Error: Invalid number of arguments. Need exactly 1 argument, the IR filename.")
