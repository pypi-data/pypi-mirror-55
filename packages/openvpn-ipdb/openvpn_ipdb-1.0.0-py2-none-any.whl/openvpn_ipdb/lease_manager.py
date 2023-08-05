
import netaddr
import os
import time

SQL_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sql')


class Lease(object):
    def __init__(self, uid=None, ip=None, last_connect=None, last_disconnect=None):
        self.uid = uid
        self.ip = str(ip)
        self.last_connect = int(last_connect) if last_connect else None
        self.last_disconnect = int(last_disconnect) if last_disconnect else None

    @staticmethod
    def from_sql(columns):
        if columns is None:
            return None
        return Lease(columns[0], columns[1], columns[2], columns[3])


class LeaseManager(object):
    def __init__(self, db, table, range_from, range_to):
        self.db = db
        self.table = table
        self.range_from = range_from
        self.range_to = range_to
        self.db.text_factory = str

    def get_lease(self, uid):
        lease = self.get_by_uid(uid)
        if lease is None:  # no lease, create new one
            ip = self.get_free_ip()
            if ip:  # found free ip
                lease = Lease(uid, ip, time.time(), None)
                self.add_lease(lease)
            else:  # no free ips, try to recycle an old ip address
                lease = self.get_oldest_unused()
                if lease is None:
                    lease = self.get_oldest_used()
                old_uid = lease.uid
                lease.uid = uid
                lease.last_connect = int(time.time())
                cursor = self.db.cursor()
                cursor.execute("UPDATE {table}"
                               " SET uid = ?, last_connect = ?"
                               " WHERE uid = ?".format(table=self.table), (lease.uid, lease.last_connect, old_uid))
                self.db.commit()
        return lease

    def get_by_uid(self, uid):
        cursor = self.db.cursor()
        cursor.execute("SELECT uid, ip, last_connect, last_disconnect"
                       " FROM {table} WHERE uid = ?".format(table=self.table), (uid,))
        return Lease.from_sql(cursor.fetchone())

    def get_by_ip(self, ip):
        cursor = self.db.cursor()
        cursor.execute("SELECT uid, ip, last_connect, last_disconnect"
                       " FROM {table} WHERE ip = ?".format(table=self.table), (ip,))
        return Lease.from_sql(cursor.fetchone())

    def get_oldest_unused(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT uid, ip, last_connect, last_disconnect"
                       " FROM {table} WHERE last_connect < last_disconnect"
                       " ORDER BY last_disconnect ASC".format(table=self.table))
        return Lease.from_sql(cursor.fetchone())

    def get_oldest_used(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT uid, ip, last_connect, last_disconnect"
                       " FROM {table} WHERE last_connect > last_disconnect"
                       " ORDER BY last_connect ASC".format(table=self.table))
        return Lease.from_sql(cursor.fetchone())

    def add_lease(self, lease):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO {table} (uid, ip, last_connect) VALUES (?, ?, ?)".format(table=self.table), (lease.uid, lease.ip, int(lease.last_connect)))
        self.db.commit()

    def get_free_ip(self):
        for ip in netaddr.iter_iprange(self.range_from, self.range_to):
            lease = self.get_by_ip(str(ip))
            if lease is None:
                return ip
        return None

    def update_disconnect(self, uid):
        cursor = self.db.cursor()
        last_disconnect = int(time.time())
        cursor.execute("UPDATE {table} SET last_disconnect = ? WHERE uid = ?".format(table=self.table), (last_disconnect, uid))
        self.db.commit()


class Ipv4LeaseManager(LeaseManager):
    def __init__(self, db, range_from, range_to):
        super(Ipv4LeaseManager, self).__init__(db, 'leases_v4', range_from, range_to)
        cursor = self.db.cursor()
        with open(os.path.join(SQL_DIRECTORY, 'leases_v4.sql'), 'r') as f:
            cursor.execute(f.read())


class Ipv6LeaseManager(LeaseManager):
    def __init__(self, db, range_from, range_to):
        super(Ipv6LeaseManager, self).__init__(db, 'leases_v6', range_from, range_to)
        cursor = self.db.cursor()
        with open(os.path.join(SQL_DIRECTORY, 'leases_v6.sql'), 'r') as f:
            cursor.execute(f.read())
