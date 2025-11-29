#!/usr/bin/env bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 [absolute path of src folder] [absolute path of target]" >&2
  echo "For example: $0 /home/[user]/openssl/ /home/[user]/openssl-cov"
  exit 1
fi


SRC=$1
TARGET=$2

LCOV_DIR=$TARGET/lcov-results
LCOV_FILE=$LCOV_DIR/coverage.info
LCOV_FILTERED=$LCOV_DIR/coverage_final.info
mkdir $LCOV_DIR

lcov --capture --directory $SRC --output-file $LCOV_FILE
lcov -r $LCOV_FILE /usr/include/\* --output-file $LCOV_FILTERED
genhtml $LCOV_FILTERED --output-directory $LCOV_DIR