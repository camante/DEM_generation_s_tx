#!/bin/bash

ncei_border_dems_path=$1
data_url_csv=$2
roi_shp=$3
resamp_res=$4
bs_dlist=$5
dem_dlist=$6

#First process any border tifs manually placed in directory.
dir_name="manual_border"
mkdir -p $dir_name
mkdir -p $dir_name/tif_orig
mkdir -p $dir_name/tif
mkdir -p $dir_name/xyz

cp tif2chunks2xyz.sh $dir_name/tif2chunks2xyz.sh
cp create_datalist.sh $dir_name/xyz/create_datalist.sh

cd $dir_name

echo "Copying over any border dems to current directory"
for file in $ncei_border_dems_path*.tif; 
do
	echo "copying file to current directory:" $file
	#[ -e $file ] && rm $file
	cp $file $(basename $file)
done


echo "Clipping Data to Outer Buffer"
for i in *.tif;
do
	gdalwarp -dstnodata -999999 -crop_to_cutline -cutline $roi_shp $i $(basename $i .tif)"_clip.tif"
	mv $i tif_orig/$i
done

echo "Converting tif to xyz"
./tif2chunks2xyz.sh 500 yes $resamp_res

cd xyz

./create_datalist.sh $dir_name
echo "$PWD/$dir_name.datalist -1 "$weight >> $bs_dlist
echo "$PWD/$dir_name.datalist -1 "$weight >> $dem_dlist

cd ..
cd ..


#Then process any NCEI DEMs online (go through 1/9th and 1/3rd tile indices)

# Get URLs from csv
IFS=,
sed -n '/^ *[^#]/p' $data_url_csv |
while read -r line
do
data_url=$(echo $line | awk '{print $1}')
resamp_var=$(echo $line | awk '{print $2}')
weight=$(echo $line | awk '{print $3}')

dir_name=$(echo $(basename $(dirname $data_url)))
mkdir -p $dir_name
mkdir -p $dir_name/tif_orig
mkdir -p $dir_name/tif
mkdir -p $dir_name/xyz

cp tif2chunks2xyz.sh $dir_name/tif2chunks2xyz.sh
cp create_datalist.sh $dir_name/xyz/create_datalist.sh

cd $dir_name

echo "Downloading Index Shp"
wget $data_url

zip_name=$(ls *.zip)
echo "Unzipping Index Shp"
unzip $zip_name

shp_name=$(ls *.shp)
echo "Index Shp name is " $shp_name
echo "ROI shp is " $roi_shp

echo "Clipping Index Shp to ROI shp"

ogr2ogr -clipsrc $roi_shp $dir_name"_"clip_index.shp $shp_name

sql_var=$dir_name"_clip_index"
echo "Dropping all Columns but URL"
#echo ogr2ogr -f "ESRI Shapefile" -sql "SELECT URL FROM \"$sql_var\"" $dir_name"_"clip_index_url.shp $dir_name"_"clip_index.shp
ogr2ogr -f "ESRI Shapefile" -sql "SELECT URL FROM \"$sql_var\"" $dir_name"_"clip_index_url.shp $dir_name"_"clip_index.shp

echo "Converting SHP to CSV"
ogr2ogr -f CSV $dir_name"_"clip_index_url.csv $dir_name"_"clip_index_url.shp

echo "Removing Header and Quotes"
sed '1d' $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv
sed 's/"//' $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv

echo "Downloading Data"
wget -c -nc --input-file $dir_name"_"clip_index_url.csv

echo "Clipping Data to Outer Buffer"
for i in *.tif;
do
	gdalwarp -dstnodata -999999 -crop_to_cutline -cutline $roi_shp $i $(basename $i .tif)"_clip.tif"
	mv $i tif_orig/$i
done


if [ "$resamp_var" == "resamp" ];
then
	echo "Resampling to finer resolution"
	echo "Converting tif to xyz"
	./tif2chunks2xyz.sh 500 yes $resamp_res
else
	echo "Keeping orig resolution"
	echo "Converting tif to xyz" 
	./tif2chunks2xyz.sh 500 no $resamp_res
fi

cd xyz

./create_datalist.sh $dir_name
echo "$PWD/$dir_name.datalist -1 "$weight >> $bs_dlist
echo "$PWD/$dir_name.datalist -1 "$weight >> $dem_dlist

cd ..
cd ..

done
