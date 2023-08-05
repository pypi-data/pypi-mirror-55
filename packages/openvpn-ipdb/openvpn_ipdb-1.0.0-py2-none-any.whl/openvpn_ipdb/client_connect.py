
import argparse
import openvpn_ipdb
import os
import sys
import syslog


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ipdb_config', help="path to ini-like configuration file")
    parser.add_argument('client_config', help='path to the OpenVPN client configuration file')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if args.debug:
        syslog.syslog(' '.join(sys.argv))

    uid = os.getenv('common_name')
    if uid is None:
        sys.stderr.write('environment variable "common_name" is not set!\n')
        sys.exit(1)

    lc = openvpn_ipdb.LeaseController(args.ipdb_config)
    with open(args.client_config, 'w') as client_config:
        lease_v4 = lc.get_lease_v4(uid)
        if lease_v4:
            client_config.write("ifconfig-push {ip} {netmask}\n".format(
                ip=lease_v4.ip,
                netmask=lc.config.get('ipv4', 'netmask')
            ))
            client_config.write("route-gateway {gateway}\n".format(gateway=lc.config.get('ipv4', 'gateway')))
        lease_v6 = lc.get_lease_v6(uid)
        if lease_v6:
            client_config.write("ifconfig-ipv6-push {ip}/{prefix_length} {gateway}\n".format(
                ip=lease_v6.ip,
                prefix_length=lc.config.get('ipv6', 'prefix_length'),
                gateway=lc.config.get('ipv6', 'gateway')
            ))
