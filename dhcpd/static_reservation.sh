#!/bin/bash

if [[ $# -ne 2 ]]; then
	echo "Not enough arguments, usage: $0 infile outfile"
	exit 1
fi

if [[ ! -f "$1" ]]; then
	echo "Error! infile does not exist!"
	exit 2
fi

if [[ ! -f "$2" ]]; then
	echo "Error! outfile does not exist!"
	exit 4
fi

while read l; do
	HOSTNAME=`echo "$l" | awk '{print $1}' -`
	MACADDR=`echo "$l" | awk '{print $2}' -`
	IPADDR=`echo "$l" | awk '{print $3'} -`
	printf "host $HOSTNAME {\n    hardware ethernet $MACADDR;\n    fixed-address $IPADDR;\n}\n" >> $2
done < $1

exit 0
