def dce(cfg):
    for function in cfg.functions:
        function = dce_function(function)

    return cfg

def dce_function(function):
    # List of registers and last-used-in instruction
    registers = []

    # TODO: Make sure that the block is being updated
    # Also make sure the correct registers are being passed

    # Maybe need to save the resulted result?
    dce_block(function.blocks[0])

    return function

def dce_block(block):
    # TODO: Maybe somehow remove instructions if they are dead code

    print("Block", block.id)
    # Stores the registers for each evaluated block
    blockRegisters = []

    # Go through all blocks that this links to
    for block in block.blocks:
        blockRegisters.append(dce_block(block, registers))

    # Get the union of the registers
    registers = []
    for regs in blockRegisters:
        registers = list(set(registers) | set(regs))

    # Go through instructions in reverse order
    for instr in block.instructions[::-1]:
        registers = dce_instruction(instr, registers)

    return registers

def dce_instruction(instr, registers):
    # Go through each type of instruction
    # Check if any registers need to be updated

    pass
