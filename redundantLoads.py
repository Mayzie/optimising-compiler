import copy
from collections import deque

def rle(cfg):
    for function in cfg.functions:
        rle_function(function)

def rle_function(function):
    # Needed for BFS
    visited = set()
    queue = deque([function.blocks[0]])
    envMap = {function.blocks[0].id: []}

    # Keeps track of whether we have hit a loop or not
    loop = 0

    # Use BFS to go through blocks
    while queue:
        block = queue.popleft()
        envList = envMap[block.id]

        # Make sure the block has all the envs it needs (if not looped yet)
        if loop < len(queue) and len(envList) != len(block.in_edges):
            queue.append(block)
            loop += 1
            continue
        loop = 0

        # Calculate intersect of envList into env
        env = []
        if envList:
            env = envList[0]
            for newEnv in envList:
                env = sorted(set(env) & set(newEnv), key = env.index)

        # Optimise the block
        rle_block(block, env)

        # Add out edge to queue if not already accounted for
        for b in block.out_edges:
            if b not in visited:
                envCopy = copy.deepcopy(env)
                if not envMap.get(b.id):
                    queue.append(b)
                    envMap[b.id] = [envCopy]
                else:
                    envMap[b.id].append(envCopy)

        # Mark as visited and remove entry in envMap
        visited.add(block)
        del envMap[block.id]

def rle_block(block, env):
    for instr in block.instructions:
        rle_instruction(instr, env)

def rle_instruction(instr, env):
    # Used to group instructions together and make if statements simpler
    instrGroup = {"add", "sub", "mul", "div", "lt", "gt", "eq"}

    # Rule 1 - If loading
    # Instructions - lc, ld
    if instr[0] == "lc":
        addToEnv(instr[1], instr[2], env)
    elif instr[0] == "ld":
        addToEnv(instr[1], instr[2], env)

    # Rule 2 - If being used/read
    # Instructions - st, add, sub, mul, div, lt, gt, eq, br, ret, call
    if instr[0] == "st":
        replaceFromEnv(2, instr, env)
    elif instr[0] in instrGroup:
        for reg in instr[2:]:
            replaceFromEnv(instr.index(reg), instr, env)
    elif instr[0] == "br":
        replaceFromEnv(1, instr, env)
    elif instr[0] == "ret":
        replaceFromEnv(1, instr, env)
    elif instr[0] == "call":
        for reg in instr[3:]:
            replaceFromEnv(instr.index(reg), instr, env)

    # Rule 3 - If being assigned (not loads)
    # Instructions - st, add, sub, mul, div, lt, gt, eq, call
    if instr[0] == "st":
        removeFromEnv(instr[1], env)
    elif instr[0] in instrGroup:
        removeFromEnv(instr[1], env)
    elif instr[0] == "call":
        removeFromEnv(instr[1], env)

# Register is added to env with links to registers of same value
def addToEnv(reg, value, env):
    reg = "r" + str(reg)
    [env.append((reg, e[0])) for e in env if value in e]
    env.append((reg, value))

# Go through env to see if register could be replaced with another register
def replaceFromEnv(i, instr, env):
    reg = "r" + str(instr[i])
    for e in env:
        if reg == e[0] and "r" in str(e[1]):
            instr[i] = e[1][1:]
            return

# Remove any elements in env referencing the register/variable
def removeFromEnv(reg, env):
    reg = "r" + str(reg) if isinstance(reg, int) else reg
    [env.remove(e) for e in [e for e in env if reg in e]]

