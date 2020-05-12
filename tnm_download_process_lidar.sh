#!/bin/bash
function help () {
echo "tnm_download_process_lidar.sh Script to download and process lidar from USGS TNM in a provided ROI shapefile"
	echo "Usage: $0 main_dir basename download_csv roi_shapefile "
	echo "* datasets_csv: <csv of datasets of interest (data_shp,filter_string,data_name,weight,laz_class(es)>"
	echo "* bs_dlist: <path to bathy surface master datalist>"
	echo "* dem_dlist: <path to dem master datalist>"
}

#see if 2 parameters were provided
#show help if not
if [ ${#@} == 4 ]; 
then
tnm_lidar_man_path=$1
datasets_csv=$2
bs_dlist=$3
dem_dlist=$4

# Get URLs from csv
IFS=,
sed -n '/^ *[^#]/p' $datasets_csv |
while read -r line
do
data_shp=$tnm_lidar_man_path$(echo $line | awk '{print $1}')
filter_string=$(echo $line | awk '{print $2}')
data_name=$(echo $line | awk '{print $3}')
weight=$(echo $line | awk '{print $4}')
first_class=$(echo $line | awk '{print $5}')
second_class=$(echo $line | awk '{print $6}')

echo "Download ROI shp is" $data_shp
echo "Filter string is" $filter_string
echo "Dataset Name is" $data_name
echo "Dataset Gridding Weight is" $weight
echo "First lidar class of interest is" $first_class
echo "Second lidar class of interest, if applicable, is" $second_class

mkdir -p $data_name

if [ -z "$second_class" ]
then
	echo "LAZ isn't topobathy and doesn't have second class"
	mkdir -p $data_name/xyz
	cp create_datalist.sh  $data_name/xyz/create_datalist.sh
	cp laz2xyz_repro_latlon_m.sh $data_name/xyz/laz2xyz_repro_latlon_m.sh
else
	echo "LAZ has valid second class"
	mkdir -p $data_name/xyz
	mkdir -p $data_name/xyz/pos
	mkdir -p $data_name/xyz/neg
	cp laz2xyz_repro_latlon_m.sh $data_name/xyz/laz2xyz_repro_latlon_m.sh
	cp separate_pos_neg.sh $data_name/xyz/separate_pos_neg.sh
	cp create_datalist.sh  $data_name/xyz/pos/create_datalist.sh
	cp create_datalist.sh  $data_name/xyz/neg/create_datalist.sh
fi

cd $data_name

echo "Getting list of laz files in shp"
fetches -R $data_shp tnm:ds=4:formats=LAZ:extents:LAZ -l > $data_name"_all.txt"

echo "Filtering list of laz files to dataset of interest"
grep -hr "$filter_string" $data_name"_all.txt" > xyz/"tnm_lidar_"$data_name".csv"
#mv "tnm_lidar_"$data_name".csv" xyz/"tnm_lidar_"$data_name".csv"

cd xyz

echo "Downloading Data"
wget -c -nc --input-file "tnm_lidar_"$data_name".csv"

echo "Converting laz to xyz for class", $first_class
./laz2xyz_repro_latlon_m.sh $first_class

if [ -z "$second_class" ]
then
	echo "LAZ isn't topobathy and doesn't have second class"
	./create_datalist.sh $data_name"_lidar"
	echo "$PWD/$data_name"_lidar".datalist -1 "$weight >> $dem_dlist
	rm *.laz
else
	echo "LAZ has valid second class"
	./laz2xyz_repro_latlon_m.sh $second_class
	echo "Separating Pos and Neg"
	./separate_pos_neg.sh
	cd pos
	./create_datalist.sh $data_name"_lidar_pos"
	echo "$PWD/$data_name"_lidar_pos".datalist -1 "$weight >> $dem_dlist
	cd ..
	cd neg 
	./create_datalist.sh $data_name"_lidar_neg"
	echo "$PWD/$data_name"_lidar_neg".datalist -1 "$weight >> $bs_dlist
	echo "$PWD/$data_name"_lidar_neg".datalist -1 "$weight >> $dem_dlist
	cd ..
	rm *.laz
fi

cd ..
cd ..

done

else
	help
fi
