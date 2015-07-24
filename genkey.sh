#!/bin/bash

DATA_DIR="$PWD/tests/data"
NAME="test"
KEY_FILE="$DATA_DIR/$NAME.key"
REQ_FILE="$DATA_DIR/$NAME.req"
CERT_FILE="$DATA_DIR/$NAME.crt"
PCKS_FILE="$DATA_DIR/$NAME.p12"
KEY_SUBJ="/C=US/ST=Denial/L=Nowhere/O=Dis/CN=123abc.test.com"
PASS="notasecret"

mkdir -p $DATA_DIR

openssl genrsa -out $KEY_FILE 2048
openssl req -new -key $KEY_FILE -out $REQ_FILE -subj $KEY_SUBJ -nodes
openssl x509 -req -days 3650 -in $REQ_FILE -signkey $KEY_FILE -out $CERT_FILE
openssl pkcs12 -keypbe PBE-SHA1-3DES -certpbe PBE-SHA1-3DES -export \
    -in $CERT_FILE -inkey $KEY_FILE                                 \
    -out $PCKS_FILE -passout pass:$PASS -name $NAME
