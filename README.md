# Team Members
- Daniel Collis
- Elie Moreau

# Programming Language
- Python 3.5.0

# Initial Configuration

Give execution permission to the program and testing script
```
chmod +x optimiser.py
chmod +x optimise.sh
chmod +x tests/run_tests.sh
```

# Running the program

Instructions on various flags and arguments for the program
```
./optimise.sh
```

# Running the tests

Execute the testing script
```
./optimise.sh <in_file> <out_file>
```

For finer grained control, run the Python program by itself:
```
./optimiser.py --help
```

# Tasks Completed

* TODO: In each section, mention if we got stuck at a particular point, or couldn't work something out, then also explain what went wrong

## Control-Flow Graph

The Control Flow graph is a relatively simple data structure. We essentially have two graphs, one
for functions, and one for blocks within those functions. The reason we chose this is because these 
two objects are intricately separate (i.e. functions reference each other, and blocks reference each
other in their local function scope). We did it this way so the unreachable code portion can operate
on entire functions (and remove them as necessary), or on individual blocks (and remove them as
necessary). 

Within the graphs, functions are connected via edges (we store both a directed graph, and an
undirected graph in the data structure). Within each function, blocks are connected via edges
(again, we store a directed graph, and an undirected graph in the data structure). The unreachable
code optimisation process utilises the undirected graph, whereas the dead code and redundant load
optimisation processes utilise the directed graph. The directed graph portion was required because 
the dead code analysis required which blocks a block links to (outgoing edge), and in redundant 
load elimination it was required to know which environment were being received from other blocks.

The control flow graph can be initialised by passing in a string (the contents of an intermediate
representation file). If the caller has passed in a string, then the control flow graph object will
parse it into control flow graph (adding the function nodes, and the block nodes for each of those
functions). To connect the graph, CFG.connect() is required to be called.

## Unreachable Code

The unreachable code optimisation process executes in three steps:

1. Finds all functions that are disconnected from the `main` function. It will then remove all of 
the disconnected functions from main, as there is no way that these can be called whatsoever 
throughout the execution of the program.
2. Iterates over each function, and finds all blocks that are disconnected from the first block 
(which may or may not be identified by id `0`). These disconnected blocks are then removed from the
function, as it is impossible for these to execute.
3. In each block, any instructions that follow a branch (`br`), or a return (`ret`) statement are
removed, as the intermediate representation specification mandates that these two statements exit
the current block.

## Dead Code Elimination

The data-flow analysis for our dead code elimination is executed on each function in the control
flow graph, since each function has its own set of live registers that don't influence other
functions.

Within each function, the dead code elimination is run in reverse order of all the instructions in
each block, passing up the set of live registers to any blocks that link to the current block.

### Transfer Functions

The transfer function is run on each block. The block will first run the transfer function on each
block that it links to, in order to retrieve the set of live registers from each of those blocks.

It will then run the merge operator on all the received sets of live registers to create the union.
Once that is created, the block will go through each of its instructions in reverse order,
updating the set of live registers as necessary at each instruction. If any instruction is flagged
for removal, then the instruction will be removed.

### Merge Operator

For the merge operator, each block will merge all the received sets of live registers from the
blocks it links to. The merge involves calculating the union of all the sets of live registers. This
is necessary as we want to keep any record of any registers being live, or possibly used.

### Instruction Analysis

For each instruction, there are two checks. The first check accounts for any instructions in which a
register is used/read. If this is the case, then the register is added to the set of live registers.

The second check accounts for any instructions in which a register is assigned to and not being
used/read. If this is the case, the register is removed from the set of live registers. If the
register wasn't in the set of live registers prior to the instruction, then the instruction is
flagged as dead code to be removed.

## Redundant Load Elimination

The data-flow analysis for our redundant load elimination is executed on each function in the
control flow graph, since each function has its own environment of registers that don't influence
other functions.

Within each function, the redundant load elimination is run using a Breadth First Search (BFS) over
every block in the current function in the control flow graph. When a block is popped off the queue
and it has all the environments needed from blocks branching to it, then the transfer function is
run on that block.

After the transfer function is run on an individual block, then the resulting environment is passed
to any blocks that require it and the BFS continues.

### Transfer Functions

The transfer function is run on each block. The block will run the instruction analysis on each
instruction, which updates the block's environment as necessary.

### Merge Operator

For the merge operator, each block will merge all the received environments from all blocks that
link to it. The merge involves calculating the insersection of all the environments. This is
necessary as we only want to keep parts of each environment that are in common, because we can
safely rely on those parts of the environments.

### Instruction Analysis

For each instruction, there are three checks. The first check accounts for any load instructions.
If this is the case, the register being loaded is added to the current block environment, with links
to any other registers that contain the same value.

The second check accounts for any instructions in which a register is used/read. If this is the
case, then the environment is checked for whether a replacement for the current register is
available. If so, then the current register is replaced with the found register.

The third case accounts for any instructions in which a register is being assigned to and is not a
load instruction. If this is the case, then the register is removed from the environment, along with
any parts of the environment that reference the register.

### Environment

The environment stores a tuple for every reference between a register and either another register,
variable, or constant. When a register is being added to the environment, the environment is checked
for any mention of the same value. Any registers that have the same value will also be referenced
when adding the register.
