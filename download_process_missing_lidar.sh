#!/bin/sh -e
function help () {
echo "process_lidar.sh Script to download and process lidar from NOAA's Digital Coast with a provided, manually edited shapefile of laz tiles"
	echo "Usage: $0 main_dir process_csv"
	echo "* main_dir: <main directory to output datalists, eg, /media/sf_external_hd/al_fl>"
	echo "* process_csv: <csv w paths to missing shps, eg., /media/sf_external_hd/al_fl/data/dc_lidar_missing_download_process.csv>"
}

#see if 2 parameters were provided
#show help if not
if [ ${#@} == 2 ]; 
then
main_dir=$1
process_csv=$2

# Get URLs from csv
IFS=,
sed -n '/^ *[^#]/p' $process_csv |
while read -r line
do
dir_name=$(echo $line | awk '{print $1}')
shp_name=$(echo $line | awk '{print $2}')
first_class=$(echo $line | awk '{print $3}')
second_class=$(echo $line | awk '{print $4}')

cd $dir_name

sql_var=$dir_name"_clip_index"
echo "Dropping all Columns but URL"
ogr2ogr -f "ESRI Shapefile" -sql "SELECT URL FROM '$sql_var'" $dir_name"_"clip_index_url.shp $dir_name"_"clip_index.shp

echo "Converting SHP to CSV"
ogr2ogr -f CSV $dir_name"_"clip_index_url.csv $dir_name"_"clip_index_url.shp

echo "Removing Header and Quotes"
sed '1d' $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv
sed 's/"//' $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv

#test out with 1 file
#head -n1 $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv

mkdir -p xyz
mv $dir_name"_"clip_index_url.csv xyz/$dir_name"_"clip_index_url.csv
cd xyz

echo "Downloading Data"
wget -c -nc --input-file $dir_name"_"clip_index_url.csv

echo "Converting laz to xyz for class", $first_class
laz2xyz.sh $first_class

if [ -z "$second_class" ]
then
	echo "LAZ isn't topobathy and doesn't have second class"
	create_datalist.sh $dir_name"_lidar"
	echo "$PWD/$dir_name"_lidar".datalist -1 1" >> $main_dir"/software/gridding/al_fl.datalist"
else
	echo "LAZ has valid second class"
	laz2xyz.sh $second_class
	echo "Separating Pos and Neg"
	separate_pos_neg.sh
	cd pos
	create_datalist.sh $dir_name"_lidar_pos"
	echo "$PWD/$dir_name"_lidar_pos".datalist -1 1" >> $main_dir"/software/gridding/al_fl.datalist"
	cd ..
	cd neg 
	create_datalist.sh $dir_name"_lidar_neg"
	echo "$PWD/$dir_name"_lidar_neg".datalist -1 1" >> $main_dir"/data/bathy/bathy_surf/al_fl_bs.datalist"
	cd ..
fi

cd ..
cd ..

done

else
	help
fi
