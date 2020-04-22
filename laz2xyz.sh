#!/bin/sh

function help () {
echo "las2xyz - A simple script that converts all .laz files in a directory to .xyz files for a provided classification"
	echo "Usage: $0 class"
	echo "* class: <the desired lidar return>
	0 Never classified
	1 Unassigned
	2 Ground
	3 Low Vegetation
	4 Medium Vegetation
	5 High Vegetation
	6 Building
	7 Low Point
	8 Reserved
	9 Water
	10 Rail
	11 Road Surface
	12 Reserved
	13 Wire - Guard (Shield)
	14 Wire - Conductor (Phase)
	15 Transmission Tower
	16 Wire-Structure Connector (Insulator)
	17 Bridge Deck
	18 High Noise"
}

total_files=$(ls -1 | grep '\.laz$' | wc -l)
echo "Total number of laz files to process:" $total_files

file_num=1

#see if 5 parameters were provided
#show help if not
if [ ${#@} == 1 ]; 
then
	#User inputs    	
	class=$1
	for i in *.laz;
	do
		#Create tmp text file of lasinfo for each lidar file
		echo "Processing File" $file_num "out of" $total_files
		echo "Processing" $i
		las2txt -i $i -keep_class $class -o $(basename $i .laz)"_class_"$class.xyz -parse xyz
		file_num=$((file_num + 1))
	done
else
	help

fi
