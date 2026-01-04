# Differential Testing Framework for MLCerts

Commit History: https://github.com/paraacha/mlcerts

Docker Images for Differential Testing Framework: https://zenodo.org/records/17850372

# Building / Set up

1. Run `build_differential_suite.sh` in the root level of this directory
   1. This will compile each of the libraries with code coverage.
   2. A .env file will be created with paths to each of the binaries. 
      1. It will also include LD_LIBRARY_PATH and PKG_CONFIG_PATH env variables which must be set in order to run the binaries.
2. Create a PEMOutputs directory following the same structure as provided.
   1. Each subdirectory must share the name of the model and include only *.pem files.

Also install lcov and lcov-parse. And set ALLOW_VERSION_1_ROOT_CERT_PARSE in cryptoConfig.h if needed for MatrixSSL (alongside removing W1,-s from test Makefile). If time virtualization is needed, install [libfaketime](https://github.com/wolfcw/libfaketime) and modify FAKETIME +
FAKETIME_LIB_PATH variables accordingly in `validate_certificate.py`. Also ensure if LD_PRELOAD needs fixing for your environment. 


# Testing
Once everything has been set up, run `run_testing.sh`.

Example: `./run_testing.sh $PROJECT_TOP_LEVEL $PROJECT_TOP_LEVEL/PEMOutputs $PROJECT_TOP_LEVEL/mlcerts $CA_FILE`

This script will run testing for all the certs in PEMOutputs, placing results into a directory called testing-results. This script will 
also collect all code coverage information. $CA_FILE can be obtained from customCA/ directory. 


You can feed the file /.../coverage.info files to report_to_json.sh to turn them into json files.


# Custom scripts:
validate_certificate.py: Performs validation of a certificate chain using all of the libraries.
compare_coverage.py: Takes in a list of coverage information in json format and creates a venn diagram.
analyze_results.py: Searches through the .json files located in `testing-results/model/json` 

All of these scripts have --help menus.

The run_testing.sh script outlines the manual process for running validation on a single library. The behavior is nested in a for-loop.


# Project Structure



```
.
. <---- THIS IS THE TOP LEVEL OF THE PROJECT (PROJECT_TOP_LEVEL)
├── coverage
│   ├── sample-model-1
│   │   ├── gnutls
│   │   │   └── lcov-results
│   │   ├── libressl
│   │   │   └── lcov-results
│   │   ├── matrixssl
│   │   │   └── lcov-results
│   │   │       └── matrixssl
│   │   ├── mbedtls
│   │   │   └── lcov-results
│   │   └── openssl
│   │       └── lcov-results
├── ignore-maps
├── include-maps
├── mlcerts
│   ├── analyze_results.py
│   ├── build_differntial_suite.sh
│   ├── build_gnutls.sh
│   ├── build_libressl.sh
│   ├── build_matrixssl.sh
│   ├── build_mbedtls.sh
│   ├── build_nettle.sh
│   ├── build_openssl.sh
│   ├── compare_coverage.py
│   ├── generate_report.sh
│   ├── gnutls
│   │   └── lcov-results
│   ├── libressl
│   │   └── lcov-results
│   ├── matrixssl
│   │   └── lcov-results
│   │       └── matrixssl
│   ├── mbedtls
│   │   └── lcov-results
│   ├── nettle
│   ├── openssl
│   │   └── lcov-results
│   ├── report_to_json.sh
│   ├── run_testing.sh
│   └── validate_certificate.py
├── PEMOutputs
│   ├── sample-model-1
└── testing-results
    └── sample-model-1
        ├── json
        └── logs
```
