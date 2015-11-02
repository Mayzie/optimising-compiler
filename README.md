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
```

# Running the program

Instructions on various flags and arguments for the program
```
./optimiser.py -h
```

# Running the tests

Execute the testing script
```
./optimise.sh
```

# Tasks Completed

* TODO: In each section, mention if we got stuck at a particular point, or couldn't work something out, then also explain what went wrong

## Control-Flow Graph

* TODO

## Unreachable Code

* TODO

## Dead Code Elimination

The data-flow analysis for our dead code elimination is executed on each function in the control
flow graph, since each function has it's own set of live registers that don't influence other
functions

Within each function, the dead code elimination is run in reverse order of all the instructions in
each block, passing up the set of live registers to any blocks that link to the current block

### Transfer Functions

The transfer function is run on each block. The block will first run the transfer function on each
block that it links to, in order to retrieve the set of live registers from each of those blocks.

It will then run the merge operator on all the received sets of registers to create the union.
Once that is created, the block will go through each of its instructions in reverse order,
updating the set of live registers as necessary at each instruction. If any instruction is flagged
for removal, then the instruction will be removed

### Merge Operator

For the merge operator, each block will merge all the received sets of registers from the blocks it
links to. The merge involves calculating the union of all the sets of registers. This is necessary
as we want to keep any record of any registers being live, or possibly used

### Instruction Analysis

For each instruction, there are two checks. The first check accounts for any instructions in which a
register is used/read. If this is the case, then the register is added to the set of live registers

The second check accounts for any instructions in which a register is assigned to and not being
used/read. If this is the case, the register is removed from the set of live registers. If the
register wasn't in the set of live registers prior to the instruction, then the instruction is
flagged as dead code to be removed

## Redundant Load Elimination

* TODO: Talk about data-flow analysis (overall)

### Lattice

* TODO

### Transfer Functions

* TODO

### Merge Operator

* TODO
