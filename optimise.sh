#!/bin/bash

if [ ! -x "optimiser.py" ] ; then
  chmod +x optimiser.py
fi

if [ $# -eq 0 ] ; then
  echo "Available optimisations:"
  echo "    - Unreachable code"
  echo "    - Dead code elimination"
  echo "    - Redundant load elimination"

  echo "For more control over the optimisation process and program, see \`./optimiser.py --help\`"
fi

if [ ! $# -eq 2 ] ; then
  echo "'$0' requires precisely 2 arguments. For more control, run \`./optimiser.py\`"

  exit 1
else
  ./optimiser.py -i $1 -o $2 -udr
fi
