#!/bin/bash

# kiírja a használati utasítást. egy paramétere van, a program neve
function print_usage_exit {
	printf "Usage: \e[1m$1\e[0m [-s] infile\n"
	printf "\t\e[1m-s\e[0m \tSkip first row\n"
	exit 1
}

if [ "`whoami`" != "root" ]; then # ellenőrzi root-ként fut-e. ha nem, kilépteti a programot.
	echo "You must be root to add new users!"
	exit 1
fi

if [[ $# -ne 1 ]]; then # van-e legalább egy argumentum
	print_usage_exit $0
fi

INFILE="" # bemeneti fájl neve
SKIP=false

if [[ $1 == "-" ]]; then # stdin-e a bemeneti fájl neve
	INFILE="/dev/stdin"
elif [[ $1 == "-s" ]]; then # jelen van-e az -s argument
	if [[ $# -ne 2 ]]; then # ha igen és nincs legalább 2 argumentuma a programnak
		print_usage_exit $0 # kilép
	fi
	INFILE=$2 # beállítja a bemeneti fájl nevét a második argumentumra
	SKIP=true
else
	INFILE=$1 # beállítja a bemeneti fájl nevét az első argumentumra
	if [[ ! -s INFILE ]]; then # ellenőrzi nem létezik-e a fájl vagy üres-e
		echo "Input file does not exists or it's empty"
		print_usage_exit $0
	fi
fi

while IFS=',' read ID PW NM; do # beolvassuk a vesszővel elválasztott ID-t, jelszót és nevet
	if $SKIP; then # ha ki kell hagynunk egy sort
		SKIP=false
		continue # kihagyjuk
	fi

	if [[ "$PW" == "#" ]]; then # random generált jelszó
		PW=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
	fi

	echo "$ID $PW $NM"
	
	useradd --comment="$NM" -m "$ID" # felhasználó hozzáad
	if [[ "$PW" != "*"]]; then
		echo "$ID:$PW" | chpasswd # jelszó megváltoztat
		(echo $PW; echo $PW) | smbpasswd -e $ID -s # samba jelszó megváltoztat
	else
		smbpasswd -e $ID -n # samba felhasználó hozzáad, jelszó nélkül
	fi
	pdbedit -f "$NM" -u $ID # teljes név megváltoztat

done < $INFILE

exit 0