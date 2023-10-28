#!/usr/bin/bash

if [ $# -ne 2 ]; then
	echo "uncorrect count of arguments"
	exit 1
fi

if g++ -o "$1" "$2"; then
	./"$2"
else
	echo "compilation error"
	exit 1
fi

