#!/usr/bin/env bash

if [ "$#" -ne 5 ]; then
  echo "Usage: $0 [path of results parent] [path to PEMOutputs] [path of mlcerts repo] [path of libs]  [ca-file]" >&2
  echo "For example: $0 /home/[user]/local /home/[user]/PEMOutputs /home/[user]/mlcerts /home/libs /home/[user]/ca.pem" >&2
  exit 1
fi
set -x

LIBRARIES=("openssl" "libressl" "gnutls" "matrixssl" "mbedtls")

TARGET_DIR=$1
PEM_OUTPUTS=$2
MLCERTS_REPO=$3
LIBRARIES_SRC=$4
CA_FILE=$5
mkdir "$TARGET_DIR"/coverage
mkdir "$TARGET_DIR"/testing-results
for model in "$PEM_OUTPUTS"/*;
do
  MODEL=${model##*/}
  mkdir "$TARGET_DIR"/testing-results/"$MODEL" && mkdir "$TARGET_DIR"/testing-results/"$MODEL"/json && mkdir "$TARGET_DIR"/testing-results/"$MODEL"/logs
  find "$LIBRARIES_SRC" -type f -name "*.gcda" -delete
  COMMAND="python3 $MLCERTS_REPO/validate_certificate.py --leaf {} --ca $CA_FILE --output-logs-dir $TARGET_DIR/testing-results/$MODEL/logs --output-json-dir $TARGET_DIR/testing-results/$MODEL/json"
  find "$PEM_OUTPUTS"/"$MODEL"/ | tail -n +2 | parallel --progress -j 100 "$COMMAND"
  mkdir "$TARGET_DIR"/coverage/"$MODEL"
  for library in "${LIBRARIES[@]}"
  do
    mkdir "$TARGET_DIR"/coverage/"$MODEL"/"$library"
    "$MLCERTS_REPO"/generate_report.sh "$LIBRARIES_SRC"/"$library" "$TARGET_DIR"/coverage/"$MODEL"/"$library"
    lcov-parse "$TARGET_DIR"/coverage/"$MODEL"/"$library"/lcov-results/coverage.info > "$TARGET_DIR"/coverage/"$MODEL"/"$library"/lcov-results/coverage.json
  done

done
set +x
echo "FINISHED"
