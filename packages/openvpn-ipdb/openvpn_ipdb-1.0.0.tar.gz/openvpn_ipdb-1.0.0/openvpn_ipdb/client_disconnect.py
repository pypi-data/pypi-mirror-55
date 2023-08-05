# -*- coding: utf-8 -*-

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
    lc.update_disconnect(uid)
