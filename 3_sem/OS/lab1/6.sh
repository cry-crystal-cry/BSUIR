#!/usr/bin/bash
if [ $# -ne 3 ]; then
	echo "uncorrect count of arguments"
	exit 1
fi

if [ -f $3 ]; then
	rm $3
fi

for file in $(find $2 -type f -user $1) 
do
	echo -e "$file, \t $(basename $file), \t $(stat $file -c "%s byte")" >>$3
done

var=$(find $2 -type f |wc -l)
echo "Total = $var"
