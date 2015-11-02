#!/bin/bash

## COMP3109 Test Suite files
## Written by Daniel Collis -- 430133523

if [ $# -le 1 ] || [ $# -gt 4 ]; then
  echo "COMP3109 Run Tests Help"
  echo "$0 <test_dir> <option> [<option> [<option>]]"
  echo "    <test_dir>  - Test folder directory"
  echo "    <option>    - Accepts three types for testing:"
  echo "                      - u (unreachable code)"
  echo "                      - d (dead code elimination)"
  echo "                      - r (redundant load elimination)"

  exit 1
else
  UNREACH=false
  DEAD=false
  REDUN=false

  case "$2" in
    u)
      UNREACH=true
      ;;
    d)
      DEAD=true
      ;;
    r)
      REDUN=true
      ;;
    *)
      echo "Invalid option '$2$'."
      exit 2
  esac

  if [ $# -gt 2 ]; then
    case "$3" in
      u)
        UNREACH=true
        ;;
      d)
        DEAD=true
        ;;
      r)
        REDUN=true
        ;;
      *)
        echo "Invalid option '$3'"
        exit 2
    esac

    if [ $# -gt 3 ]; then
      case "$4" in
        u)
          UNREACH=true
          ;;
        d)
          DEAD=true
          ;;
        r)
          REDUN=true
          ;;
        *)
          echo "Invalid option '$4'"
          exit 2
      esac
    fi
  fi

  if [ ! UNREACH ] || [ ! DEAD ] || [ ! REDUN ]; then
    echo "You did not specify an option. I don't know what to test!"
    exit 3
  fi

  TEST_DIR=$1
  UNREACH_DIR=$1"unreachable_code"
  DEAD_DIR=$1"dead_code"
  REDUN_DIR=$1"redundant_loads"

  if [ $UNREACH = true ]; then
    if [ -d $UNREACH_DIR ] ; then
      echo "====== Testing Unreachable Code ======"
      for i in $UNREACH_DIR/*.ir; do
        fname=`echo $i | grep -o ".*\\."`
        if [ -e "$fname""ex" ]; then
          ./optimiser.py --input $i --output .test.out -u
          diffcount=`sdiff -sb $i $fname"ex" | wc -L`

          if [ $diffcount -eq 0 ] ; then
            echo "Passed: $fname""ir"
          else
            echo "Failed: $fname""ir"
          fi
        fi
      done
    fi
  fi

  if [ $DEAD = true ]; then
    if [ -d $DEAD_DIR ]; then
      echo "====== Testing Dead Code Elimination ======"
      for i in $DEAD_DIR/*.ir; do
        fname=`echo $i | grep -o ".*\\."`
        if [ -e "$fname""ex" ]; then
          ./optimiser.py --input $i --output .test.out -d
          diffcount=`sdiff -sb $fname"ex" .test.out | wc -L`

          if [ $diffcount -eq 0 ]; then
            echo "Passed: $fname""ir"
          else
            echo "Failed: $fname""ir"
          fi
        fi
      done
    fi
  fi

  if [ $REDUN = true ]; then
    if [ -d $REDUN_DIR ]; then
      echo "====== Testing Redundant Load Elimination ======"
      for i in $REDUN_DIR/*.ir; do
        fname=`echo $i | grep -o ".*\\."`
        if [ -e "$fname""ex" ]; then
          ./optimiser.py --input $i --output .test.out -r
          diffcount=`sdiff -sb $fname"ex" .test.out | wc -L`

          if [ $diffcount -eq 0 ]; then
            echo "Passed: $fname""ir"
          else
            echo "Failed: $fname""ir"
          fi
        fi
      done
    fi
  fi

  if [ -e .test.out ]; then
    rm .test.out
  fi
fi
