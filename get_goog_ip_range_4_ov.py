#!/bin/env python3
#

import sys
import os
import re

GOOG_IP_RANGE = [
    "8.8.4.0/24",
    "8.8.8.0/24",
    "8.34.208.0/20",
    "8.35.192.0/20",
    "23.236.48.0/20",
    "23.251.128.0/19",
    "34.64.0.0/10",
    "35.184.0.0/13",
    "35.192.0.0/14",
    "35.196.0.0/15",
    "35.198.0.0/16",
    "35.199.0.0/17",
    "35.199.128.0/18",
    "35.200.0.0/13",
    "35.208.0.0/12",
    "35.224.0.0/12",
    "35.240.0.0/13",
    "64.15.112.0/20",
    "64.233.160.0/19",
    "66.102.0.0/20",
    "66.249.64.0/19",
    "70.32.128.0/19",
    "72.14.192.0/18",
    "74.114.24.0/21",
    "74.125.0.0/16",
    "104.154.0.0/15",
    "104.196.0.0/14",
    "104.237.160.0/19",
    "107.167.160.0/19",
    "107.178.192.0/18",
    "108.59.80.0/20",
    "108.170.192.0/18",
    "108.177.0.0/17",
    "130.211.0.0/16",
    "136.112.0.0/12",
    "142.250.0.0/15",
    "146.148.0.0/17",
    "162.216.148.0/22",
    "162.222.176.0/21",
    "172.110.32.0/21",
    "172.217.0.0/16",
    "172.253.0.0/16",
    "173.194.0.0/16",
    "173.255.112.0/20",
    "192.158.28.0/22",
    "192.178.0.0/15",
    "193.186.4.0/24",
    "199.36.154.0/23",
    "199.36.156.0/24",
    "199.192.112.0/22",
    "199.223.232.0/21",
    "207.223.160.0/20",
    "208.65.152.0/22",
    "208.68.108.0/22",
    "208.81.188.0/22",
    "208.117.224.0/19",
    "209.85.128.0/17",
    "216.58.192.0/19",
    "216.73.80.0/20",
    "216.239.32.0/19",
]
re_cidr = r'(.+)/(.*)'


def get_prefix_mask(prefix):
    quotient, remainder = divmod(prefix, 8)
    if quotient == 4:
        return '255.255.255.255'

    whole_mask = '255.' * quotient
    whole_mask += str(255 - (2 ** (8 - remainder) - 1))
    whole_mask += '.0' * max((4 - quotient - 1), 0)
    return whole_mask


def get_ip_mask_touple_list(raw):
    ip_range = []
    for i in raw:
        res = re.match(re_cidr, i)
        if res is None: continue
        ip = res.group(1)
        prefix = int(res.group(2))
        ip_range.append((ip, get_prefix_mask(prefix)))

    return ip_range


def convert_ip_range_to_openvpn_push_entry(ip_range):
    return [ f'push "route {ip} {mask}"' for ip, mask in ip_range ]


def main():
    ip_range = get_ip_mask_touple_list(GOOG_IP_RANGE)
    openvpn_push_entry = convert_ip_range_to_openvpn_push_entry(ip_range)
    routes = '\n'.join(openvpn_push_entry)
    print(routes)


if __name__ == '__main__':
    main()