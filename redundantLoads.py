import copy
from collections import deque

def rle(cfg):
    for function in cfg.functions:
        rle_function(function)

def rle_function(function):
    # Start from the first block
    rle_block(function.blocks[0], [], set())

    # Use BFS to go through blocks
    visited = set()

    queue = deque([function.blocks[0]])
    envMap = {function.blocks[0]: [set()]}

    while queue:
        block = queue.popleft()
        envList = envMap[block]

        # TODO: Make sure the block has all the envs it needs

        # TODO: Calculate intersect of envList
        env = envList[0]
        for newEnv in envList:
            env &= newEnv

        visited.add(block)

        env = rle_block(block, env)

        for b in block.blocks:
            if b not in visited:
                queue.append((b, env))



def rle_block(block, env, blocks):
    # Make sure this block hasn't been checked before
    #if block in blocks:
    #    pass
    #blocks |= {block}

    # Go through instructions
    for instr in block.instructions:
        rle_instruction(instr, env)

    print("Block", block.id, env)

    # Optimise each of the linked blocks
    # TODO: Move to rle_function() and use a BFS
    # TODO: Also Union all the env whenever multiple blocks link to one
    #for linkedBlock in block.blocks:
    #    envCopy = copy.deepcopy(env)
    #    rle_block(linkedBlock, envCopy, blocks)

def rle_instruction(instr, env):
    # Used to group instructions together and make if statements simpler
    instrGroup = {"add", "sub", "mul", "div", "lt", "gt", "eq"}

    # Rule 1 - If loading
    # Instructions - lc, ld
    # Register is added to env with links to registers of same value
    if instr[0] == "lc":
        addToEnv(instr[1], instr[2], env)
    elif instr[0] == "ld":
        addToEnv(instr[1], instr[2], env)

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
    # Instructions - st, add, sub, mul, div, lt, gt, eq, call
    # Remove any elements in env referencing the register/variable
    if instr[0] == "st":
        removeFromEnv(instr[1], env)
    elif instr[0] in instrGroup:
        removeFromEnv(instr[1], env)
    elif instr[0] == "call":
        removeFromEnv(instr[1], env)

def removeFromEnv(x, env):
    pass

def addToEnv(reg, value, env):
    reg = "r" + str(reg)
    [env.append((reg, e[0])) for e in env if value in e]
    env.append((reg, value))
