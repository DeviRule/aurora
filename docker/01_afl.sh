#!/bin/bash

# Check if an argument was provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <TIMEOUT_DURATION> <FUZZ_TARGET_PATH>"
    exit 1
fi


TIMEOUT=$1
FUZZ_TARGAT=$2

# run AFL
export CHESS=1 && timeout $TIMEOUT afl-fuzz -C -d -m none -i $EVAL_DIR/seed -o $AFL_WORKDIR -- $EVAL_DIR/$FUZZ_TARGAT 

# save crashes and non-crashes
cp $AFL_WORKDIR/default/queue/* $EVAL_DIR/inputs/crashes
cp $AFL_WORKDIR/default/non_crashes/* $EVAL_DIR/inputs/non_crashes
