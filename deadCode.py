# This is just skeleton for an algorithm idea
# I think there is a better way to do this,
# though I will need to think it through a bit more first

def dce(cfg):
    for function in cfg.functions:
        function = dce_function(function)

    return cfg

def dce_function(function):
    # List of registers and last-used-in instruction
    registers = []

    # TODO: Make sure that the block is being updated
    # Also make sure the correct registers are being passed

    # Go through the blocks in reverse order
    for block in function.blocks[::-1]:
        (block, registers) = dce_block(block, registers)

    return function

def dce_block(block, registers):
    # TODO: Maybe somehow remove instructions if they are dead code

    # Go through the instructions in reverse order
    for instr in block.instructions[::-1]:
        registers = dce_instruction(instr)

    return (block, registers)

def dce_instruction(instr):
    # TODO: Go through relevant instructions
        # If an relevant instruction is found,
        # then make the necessary changes to registers
    pass

