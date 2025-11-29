#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [absolute path of local libraries folder]" >&2
  echo "For example: $0 /home/[user]/local" >&2
  exit 1
fi
set -x
TARGET_DIR=$1
# Download mbedtls
wget https://github.com/Mbed-TLS/mbedtls/releases/download/mbedtls-3.6.1/mbedtls-3.6.1.tar.bz2 --no-check-certificate
tar jxfv mbedtls-3.6.1.tar.bz2
cd mbedtls-3.6.1 || exit
python3 -m pip install --user -r scripts/basic.requirements.txt
export CC="gcc -fsanitize=address -static-libasan -g -O1 -fno-omit-frame-pointer -fprofile-arcs -ftest-coverage"; make no_test
