echo "Creating Shps of DEM Extents"
for i in *.tif
do
echo "Processing" $i
gdal_calc.py -A $i --outfile=$(basename $i .tif)"_zero.tif"  --calc="A*0"
gdal_polygonize.py $(basename $i .tif)"_zero.tif" -f "ESRI Shapefile" $(basename $i .tif)".shp"
rm $(basename $i .tif)"_zero.tif"
echo "Created shp for" $i
#
# TO DO:
# If Not 1/9th, resample to 1/9th
# 
echo
done


echo "Merging Tifs in Name Cell Extents"
tile_extents=$1
year=2020
version=1
mkdir -p review

# Get Tile Name, Cellsize, and Extents from tile_extents_gridding.txt
IFS=,
sed -n '/^ *[^#]/p' $tile_extents |
while read -r line
do
name=$(echo $line | awk '{print $1}')
full_name=$name"_DEM_smooth_5.shp"
raster_name=$(basename $full_name .shp)".tif"
cellsize_degrees=$(echo $line | awk '{print $2}')
west=$(echo $line | awk '{print $3}')
east=$(echo $line | awk '{print $4}')
south=$(echo $line | awk '{print $5}')
north=$(echo $line | awk '{print $6}')

north_degree=${north:0:2}
north_decimal=${north:3:2}

if [ -z "$north_decimal" ]
then
	north_decimal="00"
else
	:
fi

size=${#north_decimal}
#echo "Number of North decimals is" $size
if [ "$size" = 1 ]
then
	north_decimal="$north_decimal"0
else
	:
fi

west_degree=${west:1:2}
west_decimal=${west:4:2}

if [ -z "$west_decimal" ]
then
	west_decimal="00"
else
	:
fi

size=${#west_decimal}
#echo "Number of West decimals is" $size
if [ "$size" = 1 ]
then
	west_decimal="$west_decimal"0
else
	:
fi

echo
echo "Input Tile Name is" $name
#echo "Cellsize in degrees is" $cellsize_degrees

if [ "$cellsize_degrees" = 0.00003086420 ]
then
	cell_name=19
else
	cell_name=13
fi

#add raster to vrt list
ls $(basename $full_name .shp)".tif" >> $name"_dem_list.txt"
#Create txt for all other shps

#list all shps to text
ls *.shp > $name"_shp_list.txt"
#remove shp in question
sed -i "/$full_name/d" $name"_shp_list.txt"

# #go through generated txt and clip each shp in file to the main shp
# # Get Tile Name, Cellsize, and Extents from tile_extents_gridding.txt
IFS=,
sed -n '/^ *[^#]/p' $name"_shp_list.txt" |
while read -r line
do
shp_name=$(echo $line | awk '{print $1}')

echo "Clipping" $shp_name "overlaps with" $full_name
#full_name=D_03_1_9_DEM_smooth_5.shp
#shp_name=outside.shp
output_name=$(basename $full_name .shp)"_"$(basename $shp_name .shp)"_clipped.shp"
#echo "Output_name is" $output_name
#output_name=test.shp
ogr2ogr $output_name $full_name -clipsrc $shp_name
gdalwarp -cutline $output_name -crop_to_cutline -of GTiff -dstnodata -999999 $(basename $shp_name .shp)".tif" $(basename $output_name .shp)".tif"
#ogr2ogr $name"_coast.shp" $coastline_full".shp" -clipsrc $x_min $y_min $x_max $y_max
#if shp is not empty, clip raster
rm $output_name
rm $(basename $output_name .shp)".shx"
rm $(basename $output_name .shp)".dbf"
rm $(basename $output_name .shp)".prj"

#add name to vrt list
echo "Creating VRT"
ls $(basename $output_name .shp)".tif" >> $name"_dem_list.txt"
echo "building VRT"
gdalbuildvrt -separate -input_file_list $name"_dem_list.txt" -allow_projection_difference -resolution highest $name".vrt" -overwrite
done

echo "Creating Mosaic Raster"
python ./average_tifs.py $name".vrt"

echo "Completing Final Formating of DEM"
gdalwarp -dstnodata -999999 -r average -tr $cellsize_degrees $cellsize_degrees $name"_mosaic.tif" $name"_final_tmp.tif"
gdal_translate -of GTiff -a_srs EPSG:4269 -a_nodata -999999 -co "COMPRESS=DEFLATE" -co "PREDICTOR=3" -co "TILED=YES" $name"_final_tmp.tif" "review/ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_"$year"v"$version".tif" -stats


echo "Removing Clipped tifs"
sed 1d $name"_dem_list.txt" |
while read -r line
do
clipped_tif=$(echo $line | awk '{print $1}')
#rm $clipped_tif
echo "removing" $clipped_tif
rm $clipped_tif
done

echo "Removing intermediate files"
rm $name"_shp_list.txt"
rm $name"_dem_list.txt"
rm $name".vrt"
rm $name"_mosaic.tif"
rm $name"_final_tmp.tif"
rm $name"_final_tmp.tif.aux.xml"

done
