#!/usr/bin/env bash

outto_name_prefix=${1}

./gen_openvpn_client_key_crt.sh ${outto_name_prefix}-all udp 10181
./gen_openvpn_client_key_crt.sh ${outto_name_prefix}-all-tcp tcp 10182
./gen_openvpn_client_key_crt.sh ${outto_name_prefix}-special udp 10183
./gen_openvpn_client_key_crt.sh ${outto_name_prefix}-special-tcp tcp 10184
