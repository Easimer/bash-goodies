# bash-goodies
```
/bind/webmin-dns.sh
```
Adds DNS entries from a headerless TSV file to BIND through the Webmin web interface. Needs modifications, this code has variables hardcoded to use the home.lan domain.

TSV header: FQDN (xyz.home.lan), IP
```
/dhcp/static_reservation.sh
```
Adds DHCP entries from a headerless TSV file to a dhcpd.conf file.

TSV header: Hostname, MAC address, IP address
```
/samba/samba-bulk-add.sh
```
Adds user entries to a Samba ADDC server. `infile` is a CVS file. If this file has a header, call the script with the `-s` argument.

CSV header: Username, Password, Full name

If the Password field's value is `#` (a hash) an 8 characters long, random password will be set instead or if it's value is `*` (an asterisk), no password will be set for the user.
```
/systemd/systemd-maker.py
```
An interactive script that creates "oneshot" services files for systemd. 