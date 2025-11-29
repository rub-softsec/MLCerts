#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [absolute path of local libraries folder]" >&2
  echo "For example: $0 /home/[user]/local" >&2
  exit 1
fi
set -x
TARGET_DIR=$1
# Download matrixssl
#wget https://github.com/matrixssl/matrixssl/archive/refs/tags/4-6-0-open.tar.gz --no-check-certificate
cp /attached_dir/4-6-0-open.tar.gz .  
tar xfzv 4-6-0-open.tar.gz
cd matrixssl-4-6-0-open || exit
export CC="gcc -fsanitize=address -static-libasan -g -O1 -fno-omit-frame-pointer -fprofile-arcs -ftest-coverage"; make
set +x

