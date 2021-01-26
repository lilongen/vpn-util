#!/usr/bin/env bash

get_serial() {
    curr=$(cat serial)
    new=$(( curr + 1 ))
    echo -n $new 
}

name=${1}
openssl genrsa -out ${name}.key 4096
openssl req -new -key ${name}.key -out ${name}.csr -subj "/CN=${name}/"
ser=$(get_serial)
openssl x509 -req -in ${name}.csr -out ${name}.crt -CA ca.crt -CAkey ca.key -days 3650 -set_serial ${ser}

echo -n ${ser} > serial
