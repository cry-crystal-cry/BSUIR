#!/usr/bin/bash
if [ $# -lt 2 ] && [ $# -gt 3 ]; then
    echo "uncorrect count of arguments"
    exit 0
fi

if [ ! -d $2 ]; then
 echo "there is not such folder"
 exit 0
fi

if [ $# -eq 2 ]; then 
	find "$2" -type f -not -name "*.*" -exec basename {} \; > "$1"
	exit 1
fi


find "$2" -type f -name "*.$3" -exec basename {} \; > "$1"
