# bash-goodies
```
/bind/webmin-dns.sh
```
Adds DNS entries from a headerless TSV file to BIND through the Webmin web interface. Needs modifications, this code has variables hardcoded to use the home.lan domain.

TSV header: FQDN (xyz.home.lan), IP
```
/dhcpd/static_reservation.sh
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

```
/bind/dns.py infile.csv for.domain.tld rev.domain.ltd [domcol] [ipcol]
```
Generates BIND9 forward and reverse entries based on a CSV file. `infile.csv` is the input file. `for.domain.tld` is the output forward file. `rev.domain.tld` is the output reverse file. `domcol` and `ipcol` are optional, they set the CSV column indices for the Domain and the IP address column. The default values are 6 and 4, respectively.

```
/dhcpd/static2.py infile.csv outfile.conf [namecol] [maccol] [ipcol]
```
Generates a DHCPD config file full of static address reservations based on a CSV file. `infile.csv` is the input file. `outfile.conf` is the output file. `namecol`, `maccol` and `ipcol` are optional, they set the CSV column indices for the host name, physical address and the IP address column. The default values are 0, 2 and 4, respectively.

This is the ```/dhcpd/static_reservation.sh``` script rewritten in Python.

```
/dhcpd/subnet.sh
```
Creates a DHCPD subnet definition interactively.