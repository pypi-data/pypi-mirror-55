
import ConfigParser
import openvpn_ipdb
import sqlite3


class LeaseController(object):
    def __init__(self, config_file):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self.db = sqlite3.connect(self.config.get('general', 'db'))
        self.v4lm = openvpn_ipdb.Ipv4LeaseManager(
            self.db,
            self.config.get('ipv4', 'from'),
            self.config.get('ipv4', 'to')
        )
        self.v6lm = openvpn_ipdb.Ipv6LeaseManager(
            self.db,
            self.config.get('ipv6', 'from'),
            self.config.get('ipv6', 'to')
        )

    def get_lease_v4(self, uid):
        return self.v4lm.get_lease(uid)

    def get_lease_v6(self, uid):
        return self.v6lm.get_lease(uid)

    def update_disconnect(self, uid):
        self.v4lm.update_disconnect(uid)
        self.v6lm.update_disconnect(uid)
