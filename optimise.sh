#!/bin/bash

echo "Executes the optimisation program"

testFiles=$(find tests/ -type f -name '*.ir')

for file in $testFiles; do
    echo $file
done
