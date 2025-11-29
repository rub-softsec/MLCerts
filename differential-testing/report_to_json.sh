#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [coverage file]" >&2
  echo "For example: $0 coverage.info" >&2
  exit 1
fi
set -x
INPUT_FILE=$1
lcov-parse $INPUT_FILE | jq > $INPUT_FILE.json
