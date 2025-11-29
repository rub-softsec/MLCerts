#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [absolute path of local libraries folder]" >&2
  echo "For example: $0 /home/[user]/local" >&2
  exit 1
fi
set -x
TARGET_DIR=$1
# Download openssl 
wget https://github.com/openssl/openssl/releases/download/openssl-3.3.2/openssl-3.3.2.tar.gz --no-check-certificate
# Decompress
tar zxfv openssl-3.3.2.tar.gz
cd openssl-3.3.2 || exit

export CC="gcc -fsanitize=address -g -O1 -fno-omit-frame-pointer -fprofile-arcs -ftest-coverage"; ./config --prefix=$TARGET_DIR --openssldir=$TARGET_DIR
make -j 32
make install
set +x
