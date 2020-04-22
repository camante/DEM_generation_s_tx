#!/bin/sh -e

function help () {
echo "clean_xyz- Script that removes blunders with incorrect extreme values and creates updated datalist"
	echo "Usage: $0 min_val max_val datalist_name xyz_delim"
	echo "* min_val: minimum acceptable value"
	echo "* maximum_val: maximum acceptable value"
	echo "* revert_orig: revert to original file (xyc), yes or no"
	echo "* datalist_name: datalist name to create or update"
	echo "* xyz_delim: xyz field delimiter"
}
#script to remove blunders with incorrect extreme values.
#Input files here
min_val=$1
max_val=$2
revert_orig=$3
datalist_name=$4
xyz_delim=$5

if [ "$min_val" == "help" ]
then
	help
	exit 1
else
	echo "not showing help"
fi

for i in *.xyz;
do
#input_file=0009_20080212_074447_raw.all.mb56.fbt_fix.xyz


if [ "$input_delim" == "" ]
then
	echo
	echo "IMPORTANT:"
	echo "User did not provide delimiter information. Assuming space, output will be incorrect if not actually space."
	echo
	query_delim=""
	awk_delim=""
	echo "gdal_query delim is" $query_delim
	echo "awk delim is" $awk_delim
	#exit 1
else
	echo "User input delimiter is NOT space. Taking delimiter from user input"
	query_delim="-delimiter "$input_delim
	awk_delim="-F"$input_delim
	echo "gdal_query delim is" $query_delim
	echo "awk delim is" $awk_delim
	#exit 1
fi


cp_file=$i"_ORIG.xyc"

echo "input_file is" $i
echo "cp file is" $cp_file
echo "revert to original file parameter is" $revert_orig

if [ -e $cp_file ]
then
	echo "Original Copy Already Exists"
	if [ "$revert_orig" == "yes" ]
	then
	echo "Reverting to Original File"
	rm $i
	cp $cp_file $i
	else
	echo "Cleaning most recent File"
	fi
else
	echo "Original Copy Doesn't Exist, Creating one..."
	cp $i $cp_file
fi

echo "Removing all values greater than" $min_val "and less than" $max_val

awk -v min_val="$min_val" -v max_val="$max_val" '{if ($3 > min_val && $3 < max_val) {print $1,$2,$3}}' $i > $i"tmp.xyz"
rm $i
mv $i"tmp.xyz" $i

done

echo "Creating datalist"
create_datalist.sh $datalist_name
