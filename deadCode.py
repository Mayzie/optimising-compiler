def dce(cfg):
    for function in cfg.functions:
        function = dce_function(function)

    return cfg

def dce_function(function):
    # TODO: Make sure that the block is being updated
    # Also make sure the correct registers are being passed

    # Maybe need to save the resulted result?
    result = dce_block(function.blocks[0])
    print("Function Registers:", result)

    return function

def dce_block(block):
    # TODO: Maybe somehow remove instructions if they are dead code
    # Registers contains all live registers and last-used-in instruction

    # Stores the registers at the end of this block
    registers = set()

    # Get the union of the registers (Rule 1)
    for linkedBlock in block.blocks:
        registers |= dce_block(linkedBlock)

    # Go through instructions in reverse order
    for instr in block.instructions[::-1]:
        (registers, remove) = dce_instruction(instr, registers)
        if remove:
            print("Remove is true", instr)
            # TODO: somehow remove the instruction from the block
            pass

    return registers

def dce_instruction(instr, registers):
    # Go through each type of instruction
    # Check if any registers need to be updated
    remove = False

    # Used to group instructions together and make if statements simpler
    instrGroup = {"add", "sub", "mul", "div", "lt", "gt", "eq"}

    # Rule 2
    # If being used/read
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

    # Rule 3
    # If being assigned and x is not being used/read
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

    # Rule 4
    # If no mention of register in instruction
    # Register stays in same state
    # Answer: Should be taken care of

    return (registers, remove)
