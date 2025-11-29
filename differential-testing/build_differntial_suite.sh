#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [absolute path of local libraries folder]" >&2
  echo "For example: $0 /home/[user]/local" >&2
  exit 1
fi
SRC=$(pwd)

TARGET_DIR=$1

echo "Building OpenSSL"
OPENSSL=$TARGET_DIR/openssl
mkdir $OPENSSL && cd $OPENSSL && $SRC/build_openssl.sh $OPENSSL && export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$OPENSSL/lib && cd $SRC && echo "OPENSSL=$OPENSSL/bin/openssl" >>.env || exit 1

echo "Building LibreSSL"
LIBRESSL=$TARGET_DIR/libressl
mkdir $LIBRESSL && cd $LIBRESSL && $SRC/build_libressl.sh $LIBRESSL && cd $SRC && echo "LIBRESSL=$LIBRESSL/bin/openssl" >>.env || exit 1

echo "Building MatrixSSL"
MATRIXSSL=$TARGET_DIR/matrixssl
mkdir $MATRIXSSL && cd $MATRIXSSL && $SRC/build_matrixssl.sh $MATRIXSSL && cd $SRC && echo "MATRIXSSL=$MATRIXSSL/matrixssl-4-6-0-open/matrixssl/test/certValidate" >>.env || exit 1

echo "Building Nettle"
NETTLE=$TARGET_DIR/nettle
mkdir $NETTLE && cd $NETTLE && $SRC/build_nettle.sh $NETTLE && export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$NETTLE/lib64 && export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:$NETTLE/lib64/pkgconfig && cd $SRC || exit 1

echo "Building GNUTLS"
GNUTLS=$TARGET_DIR/gnutls
mkdir $GNUTLS && cd $GNUTLS && $SRC/build_gnutls.sh $GNUTLS && cd $SRC && echo "GNUTLS=$GNUTLS/bin/certtool" >>.env || exit 1

echo "Building MBEDTLS"
MBEDTLS=$TARGET_DIR/mbedtls
mkdir $MBEDTLS && cd $MBEDTLS && $SRC/build_mbedtls.sh $MBEDTLS && cd $SRC && echo "MBEDTLS=$MBEDTLS/mbedtls-3.6.1/programs/x509/cert_app" >> .env || exit 1

echo "LD_LIBRARY_PATH=$OPENSSL/lib64:$NETTLE/lib64" >>.env && echo "PKG_CONFIG_PATH=$NETTLE/lib64/pkgconfig" >>.env || exit 1

echo "Finished!"
