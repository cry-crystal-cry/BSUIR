rm log.txt
diff -i $1 $2  &> log.txt
Errorlevel=$?
if [ $Errorlevel == 2 ]
	then
		echo "compare error"
	elif [ $Errorlevel == 1 ]
		then 
		echo "files are not the same"
		rm $2
		attrib +h $1
	else
		echo "same files"
		cat $1
		echo ""
fi
read -s -n 1 -p "pause..."
