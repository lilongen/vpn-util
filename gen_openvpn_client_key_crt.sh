#!/usr/bin/env bash

get_serial() {
    if [ ! -f serial ]; then
        echo -n 101
        return
    fi
    curr=$(cat serial)
    new=$(( curr + 1 ))
    echo -n $new 
}

outto_name=${1}
outto="client_config/${outto_name}"
if [ -d ${outto} ]; then
    echo "folder ${outto} already exists!!!"
    exit 1
fi

mkdir -p ${outto}
file_name="${outto}/client"
openssl genrsa -out ${file_name}.key 4096
openssl req -new -key ${file_name}.key -out ${file_name}.csr -subj "/CN=${outto_name}/"
ser=$(get_serial)
openssl x509 -req -in ${file_name}.csr -out ${file_name}.crt -CA ca.crt -CAkey ca.key -days 3650 -set_serial ${ser}
echo -n ${ser} > serial

cp ca.crt ${outto}/
cp config.ovpn ${outto}/${outto_name}.ovpn
cp ta.key ${outto}/
