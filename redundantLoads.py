def rle(cfg):
    for function in cfg.functions:
        rle_function(function)

def rle_function(function):
    # Start from the first block
    rle_block(function.blocks[0], [], set())

def rle_block(block, env, blocks):
    # Make sure this block hasn't been checked before
    if block in blocks:
        pass
    blocks |= {block}

    # Go through instructions
    for instr in block.instructions:
        rle_instruction(instr, env)

    # Optimise each of the linked blocks
    for linkedBlock in block.blocks:
        rle_block(linkedBlock, env)

def rle_instruction(instr, env):
    # Used to group instructions together and make if statements simpler
    instrGroup = {"add", "sub", "mul", "div", "lt", "gt", "eq"}

    # Rule 1 - If loading
    # Instructions - lc, ld
    # Register is added to env with links to registers of same value
    if instr[0] == "lc":
        pass
    elif instr[0] == "ld":
        pass

    # Rule 2 - If being used/read
    # Instructions - st, add, sub, mul, div, lt, gt, eq, br, ret, call
    # Go through env to see if register could be replaced with another register
    if instr[0] == "st":
        pass
    elif instr[0] in instrGroup:
        pass
    elif instr[0] == "br":
        pass
    elif instr[0] == "ret":
        pass
    elif instr[0] == "call":
        pass

    # Rule 3 - If being assigned (not loads)
    # Instructions - add, sub, mul, div, lt, gt, eq, call
    # Remove any elements referencing the register
    if instr[0] in instrGroup:
        pass
    elif instr[0] == "call":
        pass
