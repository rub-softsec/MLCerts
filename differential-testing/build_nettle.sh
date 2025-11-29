#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [absolute path of local libraries folder]" >&2
  echo "For example: $0 /home/[user]/local" >&2
  exit 1
fi
set -x
TARGET_DIR=$1
# Download nettle
wget https://ftp.gnu.org/gnu/nettle/nettle-3.6.tar.gz --no-check-certificate
tar zxfv nettle-3.6.tar.gz
cd nettle-3.6 || exit
export CC="gcc -fprofile-arcs -ftest-coverage"; ./configure --prefix=$TARGET_DIR --disable-openssl --enable-shared --enable-mini-gmp
make -j 32
make install
set +x



