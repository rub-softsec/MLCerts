#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [absolute path of local libraries folder]" >&2
  echo "For example: $0 /home/[user]/local" >&2
  exit 1
fi
set -x
TARGET_DIR=$1
# Download libressl
wget https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-3.9.2.tar.gz --no-check-certificate
tar zxfv libressl-3.9.2.tar.gz
cd libressl-3.9.2 || exit
export CC="gcc -fsanitize=address -static-libasan -g -O1 -fno-omit-frame-pointer -fprofile-arcs -ftest-coverage"; ./config --prefix=$TARGET_DIR --openssldir=$TARGET_DIR
make -j 32
make install
set +x
