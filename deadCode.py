def dce(cfg):
    for function in cfg.functions:
        dce_function(function)

def dce_function(function):
    # Start from the first block
    dce_block(function.blocks[0])

def dce_block(block):
    # Stores the live registers throughout the block
    registers = set()

    # Get the union of the registers (Rule 1)
    for linkedBlock in block.blocks:
        registers |= dce_block(linkedBlock)

    # Go through instructions in reverse order
    for instr in block.instructions[::-1]:
        remove = dce_instruction(instr, registers)
        # Remove any instruction if needed
        # TODO: Maybe a bug if some instructions are the same?
        if remove:
            block.instructions.remove(instr)

    return registers

def dce_instruction(instr, registers):
    # If this instruction needs to be removed (dead code)
    remove = False

    # Used to group instructions together and make if statements simpler
    instrGroup = {"add", "sub", "mul", "div", "lt", "gt", "eq"}

    # Rule 2 - If being used/read
    # Instructions: st, add, sub, mul, div, lt, gt, eq, br, ret, call
    # Register becomes live (if not live already)
    if instr[0] == "st":
        registers |= {instr[2]}
    elif instr[0] in instrGroup:
        registers |= {instr[2], instr[3]}
    elif instr[0] == "br":
        registers |= {instr[1]}
    elif instr[0] == "ret":
        registers |= {instr[1]}
    elif instr[0] == "call":
        registers |= {instr[3:]}

    # Rule 3 - If being assigned and x is not being used/read
    # Instructions: lc, ld, and maybe add, sub, mul, div, lt, gt, eq, call
    # Register becomes dead (make sure that register is not used/read as well)
    if instr[0] == "lc":
        if instr[1] not in registers:
            remove = True
        registers -= {instr[1]}
    elif instr[0] == "ld":
        if instr[1] not in registers:
            remove = True
        registers -= {instr[1]}
    elif instr[0] in instrGroup:
        if instr[1] not in registers:
            remove = True
        if instr[1] not in {instr[2:4]}:
            registers -= {instr[1]}
    elif instr[0] == "call":
        if instr[1] not in registers:
            remove = True
        if instr[1] not in {instr[3:]}:
            registers -= {instr[1]}

    return remove
