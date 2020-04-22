#!/bin/sh

function help () {
echo "lidar2tif2xyz - A simple script that converts all .laz files in a directory to .tif files and then to xyz for a provided classification and cell size."
	echo "Usage: $0 class cellsize"
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
	echo "* cellsize: <cell size in arc-seconds>
	0.0000102880663/0.0000102880663 = 1/27 arc-second
	0.00003086420/0.00003086420 = 1/9th arc-second 
	0.0000925925/0.0000925925 = 1/3rd arc-second"
}

#see if 6 parameters were provided
#show help if not
#get count of laz files
total_files=$(ls -1 | grep '\.laz$' | wc -l)
echo "Total number of laz files to process:" $total_files

file_num=1

if [ ${#@} == 2 ]; 
then
	#User inputs    	
	class=$1
	cellsize=$2
	for i in *.laz;
	do
		#Create tmp text file of lasinfo for each lidar file
		#"$(lasinfo $i)" > lasinfo_tmp.txt
		echo "Processing File" $file_num "out of" $total_files
		echo "Processing" $i
		lasinfo $i -stdout > lasinfo_tmp.txt
	
		#Get minx, maxx, miny, maxy from temporary file
		minx="$(grep -e "min x" lasinfo_tmp.txt | awk '{print $5}')"
		maxx="$(grep -e "max x" lasinfo_tmp.txt | awk '{print $5}')"
		miny="$(grep -e "min x" lasinfo_tmp.txt | awk '{print $6}')"
		maxy="$(grep -e "max x" lasinfo_tmp.txt | awk '{print $6}')"
		
		echo "Determining if the following class exits: class" $class
		las2txt -i $i -keep_class $class -o $i.txt 

		if [ -s $i.txt ]
		then 
		   echo "File contains returns of class " $class
		   echo "Converting $i to tif..."
		   gmt xyz2grd $i.txt -R${minx}/${maxx}/${miny}/${maxy} -G$(basename $i .las)"_class_"$class".tif"=gd:GTiFF -I$cellsize
		   rm $i.txt 
		   echo "Converting $i.tif to xyz..."
		   gdal_translate -of XYZ $(basename $i .las)"_class_"$class".tif" $(basename $i .las)"_class_"$class"_tmp.xyz"
		   echo "Removing null values"
		   grep -v "nan" $(basename $i .las)"_class_"$class"_tmp.xyz" | awk '{printf "%.8f %.8f %.3f\n", $1,$2,$3}' > $(basename $i .las)"_class_"$class".xyz"
		   rm $(basename $i .las)"_class_"$class"_tmp.xyz"
		   #rm $i
		else
		   echo "File DOES NOT contains returns of class " $class
		   rm $i.txt
		   #rm $i
		fi
		file_num=$((file_num + 1))
		echo
		echo
		rm lasinfo_tmp.txt
	done

else
	help

fi

