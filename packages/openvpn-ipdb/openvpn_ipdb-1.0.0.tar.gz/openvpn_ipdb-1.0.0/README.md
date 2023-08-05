# OpenVPN IPdb

This python package provides a small tool for managing OpenVPN IP addresses.


## Configuration

Create instance configuration ini file (see `ipdb.dist.ini` for all configuration possibilities):
```ini
[general]
db = /var/lib/ipdb.sqlite

[ipv4]
from = 192.168.1.100
to   = 192.168.1.199
netmask = 255.255.255.0
gateway = 192.168.1.1

[ipv6]
from = fd00::1000
to = fd00::1fff
prefix_length = 64
gateway = fd00::1/64
```


## Usage

Add the following lines to your OpenVPN configuration (replace the paths to the actual script and ini file):

```
client-connect "/usr/local/bin/ipdb-client-connect /etc/ipdb.ini"
client-disconnect "/usr/local/bin/ipdb-client-disconnect /etc/ipdb.ini"
```
