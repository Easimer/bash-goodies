#!/bin/bash

function add_subnet {
	tf=$1
	read -p "Add a subnet? " -i "yes" -e CH
	if [[ $CH != "yes" ]]; then
		return 1
	fi
	read -p "Network address (dotted decimal): " -e NETADDR
	read -p "Network mask (dotted decimal): " -e NETMASK
	echo "subnet $NETADDR netmask $NETMASK {" > $tf
	read -p "Address range (leave empty if there's none): " -e RANGE
	if [[ $#RANGE -gt 0 ]]; then
		echo "range $RANGE;"
	fi
	read -p ""
	return 0
}

tf=$(mktemp /tmp/.dhcpsubnet.XXXXX)

read -p "Domain (leave empty if there's none): " -e DOMAIN
if [[ $#DOMAIN -gt 0 ]]; then
	echo "option domain-name \"$DOMAIN\";" > $tf
fi
read -p "Nameservers (separated by colon. leave empty if there's none): " -e NS
if [[ $#NS -gt 0 ]]; then
	echo "option domain-name-servers \"$NS\";" > $tf
fi

read -p "Authoritative? (yes or no)" -i "yes" -e AUTH
if [[ "$AUTH" == "yes" ]]; then
	echo "authoritative;" > $tf
fi

read -p "Default lease time: " -i 600 -e DLT
echo "default-lease-time $DLT;" > $tf

read -p "Maximum lease time: " -i 600 -e MLT
echo "max-lease-time $MLT;" > $tf

while add_subnet $tf; do :; done

rm "$tf"