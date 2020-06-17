#!/bin/bash

export PKG_DIR="dynamodb-client/python"

rm -rf ${PKG_DIR} && mkdir -p ${PKG_DIR}

## We need to download and compile libraries which are compatible with Amazon Linux Image
## so we are using Lambda docker image, downloading the libraries 
docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.7 \
    pip install -r requirements.txt -t ${PKG_DIR}
