#!/usr/bin/env python3
#

import sys
import re
import yaml


yaml_file = sys.argv[1]
with open(yaml_file) as f:
    goog_cidr = yaml.load(f)

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
    ip_range = get_ip_mask_touple_list(goog_cidr)
    openvpn_push_entry = convert_ip_range_to_openvpn_push_entry(ip_range)
    routes = '\n'.join(openvpn_push_entry)
    print(routes)


if __name__ == '__main__':
    main()