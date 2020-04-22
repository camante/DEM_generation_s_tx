#!/bin/sh 
function help () {
echo "process_lidar.sh Script to download and process lidar from NOAA's Digital Coast in a provided ROI shapefile"
	echo "Usage: $0 main_dir basename download_csv roi_shapefile "
	echo "* main_dir: <main directory to output datalists, eg, /media/sf_external_hd/al_fl>"
	echo "* basename: <basename for datalist, e.g. w_fl>" 
	echo "* download_csv: <csv w urls of bulk_download tileindex.zip>"
	echo "* roi_shp: <user-provided shp of your ROI>"
}

#see if 2 parameters were provided
#show help if not
if [ ${#@} == 4 ]; 
then
main_dir=$1
basename=$2
data_url=$3
roi_shp=$4

# Get URLs from csv
IFS=,
sed -n '/^ *[^#]/p' $data_url |
while read -r line
do
data_url=$(echo $line | awk '{print $1}')
first_class=$(echo $line | awk '{print $2}')
second_class=$(echo $line | awk '{print $3}')

dir_name=$(echo $(basename $(dirname $data_url)))
mkdir -p $dir_name
cd $dir_name

echo "Downloading Index Shp"
wget $data_url

echo "Unzipping Index Shp"
unzip tileindex.zip

shp_name=$(ls *.shp)
echo "Index Shp name is " $shp_name

echo "Clipping Index Shp to ROI shp"
ogr2ogr -clipsrc $roi_shp $dir_name"_"clip_index.shp $shp_name

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
	echo "$PWD/$dir_name"_lidar".datalist -1 1" >> $main_dir"/software/gridding/"$basename".datalist"
	rm *.laz
else
	echo "LAZ has valid second class"
	laz2xyz.sh $second_class
	echo "Separating Pos and Neg"
	separate_pos_neg.sh
	cd pos
	create_datalist.sh $dir_name"_lidar_pos"
	echo "$PWD/$dir_name"_lidar_pos".datalist -1 1" >> $main_dir"/software/gridding/"$basename".datalist"
	cd ..
	cd neg 
	create_datalist.sh $dir_name"_lidar_neg"
	echo "$PWD/$dir_name"_lidar_neg".datalist -1 1" >> $main_dir"/data/bathy/bathy_surf/"$basename"_bs.datalist"
	cd ..
	rm *.laz
fi

cd ..
cd ..

done

else
	help
fi
