#!/usr/bin/env python3

import argparse
from dotenv import load_dotenv
load_dotenv()
import os
import sys
from abc import ABC, abstractmethod
from enum import Enum
from subprocess import Popen, PIPE
from typing import Tuple
import json

FAKETIME = "2022-06-15 11:22:23"
FAKETIME_LIB_PATH = "/attached_dir/LIBS/libfaketime/src/libfaketime.so.1"
my_env = os.environ.copy()
if "LD_PRELOAD" in my_env:
    my_env["LD_PRELOAD"] = FAKETIME_LIB_PATH + ":" + my_env["LD_PRELOAD"]
else:
    my_env["LD_PRELOAD"] = FAKETIME_LIB_PATH
openssl_env = os.environ.copy()
if "LD_PRELOAD" in openssl_env:
    openssl_env["LD_PRELOAD"] = "/lib/x86_64-linux-gnu/libasan.so.6:" + FAKETIME_LIB_PATH + ":" + my_env["LD_PRELOAD"]
else:
    openssl_env["LD_PRELOAD"] = "/lib/x86_64-linux-gnu/libasan.so.6:" + FAKETIME_LIB_PATH
#my_env["LD_PRELOAD"] = FAKETIME_LIB_PATH + ":" + my_env["LD_PRELOAD"]
my_env["FAKETIME"] = FAKETIME
openssl_env["FAKETIME"] = FAKETIME

DEBUG = 0

parser = argparse.ArgumentParser(
    description="Validate a certificate against a suite of TLS implementations."
)


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


parser.add_argument("--leaf", "-l", type=file_path, action="store", required=True)
parser.add_argument("--ca", "-ca", type=file_path, action="store", required=True)
parser.add_argument("--verbose", "-v", action="store_true", required=False)
parser.add_argument(
    "--output-logs-dir", type=dir_path, action="store", required=False, default="."
)
parser.add_argument(
    "--output-json-dir", type=dir_path, action="store", required=False, default="."
)


class VerificationResult(Enum):
    SUCCESS = 0
    FAILURE = 1
    CRASH = 2


class VerifyCertificateBase(ABC):
    def __init__(self):
        class_name = self.__class__.__name__
        self.binary = os.environ.get(class_name.upper())
        if self.binary is None:
            raise ValueError(f"Cannot find binary for {class_name}")

    @abstractmethod
    def verify(self, leaf: str, ca: str) -> Tuple[int, bytes, bytes]:
        pass


class OpenSSL(VerifyCertificateBase):
    def verify(self, leaf: str, ca: str) -> Tuple[int, bytes, bytes]:
        process = Popen(
            [self.binary, "verify", "-CAfile", ca, "-untrusted", leaf, leaf], stderr=PIPE, stdout=PIPE, env=openssl_env
        )
        stdout, stderr = process.communicate()

        return process.wait(), stdout, stderr


class LibreSSL(VerifyCertificateBase):
    def verify(self, leaf: str, ca: str) -> Tuple[int, bytes, bytes]:
        process = Popen(
            [self.binary, "verify", "-CAfile", ca, "-untrusted", leaf, leaf], stderr=PIPE, stdout=PIPE, env=my_env
        )
        stdout, stderr = process.communicate()

        return process.wait(), stdout, stderr

class GNUTLS(VerifyCertificateBase):
    def verify(self, leaf: str, ca: str) -> Tuple[int, bytes, bytes]:

        with open(leaf, "r") as f:
            # ls if we want to allow sha1 or md5
            process = Popen(
                [self.binary, "--verify", "--load-ca-certificate", ca],
                stderr=PIPE,
                stdout=PIPE,
                stdin=f,
                env=my_env
            )
            stdout, stderr = process.communicate()

            return process.wait(), stdout, stderr


class MBEDTLS(VerifyCertificateBase):
    def verify(self, leaf: str, ca: str) -> Tuple[int, bytes, bytes]:
        process = Popen(
            [self.binary, "mode=file", f"filename={leaf}", f"ca_file={ca}"],
            stderr=PIPE,
            stdout=PIPE,
            env=my_env
        )
        stdout, stderr = process.communicate()
        ret = process.wait()
        if ret != 0:
            return ret, stdout, stderr
        error_code = 0 if b"failed" not in stdout else 1

        return error_code, stdout, stderr


class MatrixSSL(VerifyCertificateBase):
    def verify(self, leaf: str, ca: str) -> Tuple[int, bytes, bytes]:
        process = Popen(
            [self.binary, "-c", ca, leaf],
            stderr=PIPE,
            stdout=PIPE,
            env=my_env
        )
        stdout, stderr = process.communicate()
        ret = process.wait()
        return ret, stdout, stderr


SSL_LIBRARIES = [OpenSSL, LibreSSL, GNUTLS, MBEDTLS, MatrixSSL]

if __name__ == "__main__":
    args = parser.parse_args()
    leaf_cert = args.leaf
    ca_cert = args.ca
    output = {}

    output_file_base = os.path.basename(leaf_cert)

    for library in SSL_LIBRARIES:
        try:
            library_name = library.__name__
            verification_output = library().verify(leaf_cert, ca_cert)
            output[library_name] = verification_output[0]

            with open(
                f"{args.output_logs_dir}/{output_file_base}-{library_name.lower()}.log",
                "wb",
            ) as f:
                f.write(verification_output[1])
                f.write(verification_output[2])

        except ValueError as ve:
            if args.verbose:
                print(ve, file=sys.stderr)

    with open(f"{args.output_json_dir}/{output_file_base}.json", "w") as f:
        f.write(json.dumps(output) + "\n")
