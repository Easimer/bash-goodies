#!/bin/bash

IP="https://localhost:10000"

function login {
	exec 3>&1;
	IP=$(dialog --title "Webmin Login" --inputbox "Webmin address:" 8 50 2>&1 1>&3)
	USERNAME=$(dialog --title "Webmin Login" --inputbox "Username:" 8 50 2>&1 1>&3)
	PASSWORD=$(dialog --title "Webmin Login" --passwordbox "Password: (will be invisible)" 8 50 2>&1 1>&3)
	exec 3>&-;
	clear
	curl -c "/tmp/.cookies" -s "$IP" -k
	curl -c "/tmp/.cookies" -b "/tmp/.cookies" -s "$IP/session_login.cgi" -k -d "user=$USERNAME&pass=$PASSWORD&page=/" -X POST -H 'Cookie: testing=1'
}

# add entry
function add {
	NAME=$1
	IP=$2
	curl -b "/tmp/.cookies" -s "https://rpi.home.lan:10000/bind8/save_record.cgi?zone=home.lan&view=any&file=%2Fetc%2Fbind%2Ffor.home.lan&origin=home.lan&sort=&new=1&type=A&redirtype=A&name=${NAME}&ttl_def=1&ttlunit=&value0=${IP}&comment=&rev=1" -k -X GET -H "Referer: https://rpi.home.lan:10000"
}

if [[ $# -ne 1 ]]; then
	echo "Not enough arguments, usage: $0 infile"
	exit 1
fi

if [[ ! -f "$1" ]]; then
	echo "Error! infile does not exist!"
	exit 2
fi

login
while read l; do
	NAME=`echo "$l" | awk '{print $1}' -`
	IP=`echo "$l" | awk '{print $2}' -`
	add $NAME $IP
done < $1

if [[ -f "/tmp/.cookies" ]]; then
	rm /tmp/.cookies
fi
