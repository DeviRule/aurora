#!/bin/bash

set -eu

# go to directory
cd $AURORA_GIT_DIR/root_cause_analysis

# Build components
cargo build --release --bin monitor
cargo build --release --bin rca

# run root cause analysis
CHESS= 1 cargo run --release --bin rca -- --eval-dir $EVAL_DIR --trace-dir $EVAL_DIR --monitor --rank-predicates

# (Optional) enrich with debug symbols
CHESS=1 cargo run --release --bin addr2line -- --eval-dir $EVAL_DIR
