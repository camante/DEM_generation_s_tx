#!/bin/bash

function help () {
echo "pos2neg- Script that converts third column in xyz file from positive to negative by multiplying by -1"
	echo "Usage: $0 delim "
	echo "* delim; if not provided then space is assumed"
}

delim=$1

if [ "$delim" == "" ]
then
	echo
	echo "IMPORTANT:"
	echo "User did not provide delimiter information. Assuming space, output will be incorrect if not actually space."
	echo
	param=""
else
	echo "User input delimiter is NOT space. Taking delimiter from user input"
	param="-F"$delim
fi

total_files=$(ls -1 | grep '\.xyz$' | wc -l)
echo "Total number of xyz files to process:" $total_files
file_num=1

mkdir -p neg

#unzip "*.ZIP"
#move all files up to main dir
#find . -mindepth 2 -type f -print -exec mv {} . \;
for i in *.xyz;
do
echo "Processing File" $file_num "out of" $total_files
echo "File name is " $i
awk $param '{printf "%.8f %.8f %.3f\n", $1,$2,$3*-1}' $i > "neg/"$(basename $i .xyz)"_neg.xyz"
echo

file_num=$((file_num + 1))
done

