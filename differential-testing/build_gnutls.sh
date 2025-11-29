#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [absolute path of local libraries folder]" >&2
  echo "For example: $0 /home/[user]/local" >&2
  exit 1
fi
set -x
TARGET_DIR=$1
# Download gnutls
wget https://www.gnupg.org/ftp/gcrypt/gnutls/v3.7/gnutls-3.7.11.tar.xz --no-check-certificate
tar xfv gnutls-3.7.11.tar.xz
cd gnutls-3.7.11 || exit
export CC="gcc -fsanitize=address -static-libasan -g -O1 -fno-omit-frame-pointer -fprofile-arcs -ftest-coverage"; ./configure --prefix=$TARGET_DIR --disable-doc --with-included-libtasn1 --with-included-unistring --without-p11-kit
make clean && make -j 32 && make -C fuzz check && make code-coverage-capture CODE_COVERAGE_IGNORE_PATTERN='*/include/*' && make install
set +x
