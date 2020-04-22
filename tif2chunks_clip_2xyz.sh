#!/bin/sh
function help () {
echo "tif2chunks2xyz.sh - A script that converts all tif files in a directory to smaller chunks and then to xyz."
	echo "Usage: $0 chunk_dims resamp cellsize"
	echo "* chunk_dims: <number of rows/columns per chunk in resamp resolution>"
	echo "* resamp: <resample the tif, yes or no>"
	echo "* cellsize: <resampled cell size in arc-seconds>
	0.0000102880663 = 1/27 arc-second
	0.000030864199 = 1/9th arc-second 
	0.000092592596 = 1/3rd arc-second
	1 = 1 arc-second"
	echo "* shp: <shapefile for clipping. Don't include .shp extension >"
	echo "* invert: <invert shapefile for clipping, yes or no>"


}

if [ ${#@} == 5 ]; 
then


mkdir -p tif_clip
mkdir -p xyz

#Example, create chunks 150 rows by 150 cols
chunk_dim_x_int=$1
chunk_dim_y_int=$1
resamp_input=$2
resamp_res=$3
shp_full=$4
invert=$5


if [ "$invert" == "yes" ];
then
	echo -- Inverting clip
	invert_param="-i"
else
	echo -- Not Inverting clip
	invert_param=
fi


six_cells_target=$(echo "$resamp_res * 6" | bc -l)

#get count of tif files
total_files=$(ls -1 | grep '\.tif$' | wc -l)
echo "Total number of tif files to process:" $total_files

file_num=1
for i in *.tif;
do
	echo "Processing File" $file_num "out of" $total_files
	echo "Processing" $i

	if [ "$resamp_input" == "yes" ];
	then
		echo -- Resampling to target resolution in NAD83
		#exit 1
		gdalwarp $i -dstnodata -999999 -r cubicspline -tr $resamp_res $resamp_res -t_srs EPSG:4269 $(basename $i .tif)"_resamp.tif" -overwrite
		mv $i $(basename $i .tif)"_orig.tif"
		mv $(basename $i .tif)"_resamp.tif" $i
	else
		echo -- Keeping orig resolution
		gdalwarp $i -dstnodata -999999 $i"tmp.tif"
		mv $i $(basename $i .tif)"_orig.tif"
		mv $i"tmp.tif" $i
		
		#exit 1
	fi

	#Clip with shapefile
	echo -- Masking out shp
	gdal_rasterize -burn -999999 $invert_param -l $shp_full $shp_full".shp" $i

	#get input grid dimensions
	x_dim=`gdalinfo $i | grep -e "Size is" | awk '{print $3}' | sed 's/.$//'`
	y_dim=`gdalinfo $i | grep -e "Size is" | awk '{print $4}'`
	
	echo chunk x_dim is $chunk_dim_x_int
	echo chunk y_dim is $chunk_dim_y_int

	echo
	echo -- Starting Chunk Analysis
	echo

	#initiate chunk names with numbers, starting with 1
	chunk_name="1"
	#remove file extension to get basename from input file
	input_name=${i::-4}
	#starting point for tiling
	xoff=0
	yoff=0

	while [ "$(bc <<< "$xoff < $x_dim")" == "1"  ]; do
	    yoff=0
	    while [ "$(bc <<< "$yoff < $y_dim")" == "1"  ]; do
	    chunk_name_full=$input_name"_chunk_"$chunk_name".tif"
	    chunk_name_full_clip=$input_name"_chunk_"$chunk_name"_clip.tif"
	    echo creating chunk $chunk_name_full_clip
	    echo xoff is $xoff
	    echo yoff is $yoff
	    echo chunk_dim_x_int is $chunk_dim_x_int
	    echo chunk_dim_y_int $chunk_dim_y_int
	    gdal_translate -of GTiff -srcwin $xoff $yoff $chunk_dim_x_int $chunk_dim_y_int $i $chunk_name_full_clip -stats
	    valid_check=
	    valid_check=`gdalinfo $chunk_name_full_clip | grep -e "STATISTICS_MAXIMUM"`
	    #valid_check=`gdalinfo $chunk_name_full_clip -mm | grep -e "Computed " | awk '{print $2}' | awk -F',' '{print $2}'`
	    echo "Valid check is" $valid_check
	    #exit 1

	    if [[ -z "$valid_check" ]];
		then
		    echo "chunk has no data, deleting..."
		    rm $chunk_name_full_clip
		else
		    echo "chunk has data, keeping..."
			#Convert to xyz if valid data.
		  	echo -- Converting to xyz
		    gdal_translate -of XYZ $chunk_name_full_clip $chunk_name_full_clip"_tmp.xyz"
		    awk '{if ($3 > -99999 && $3 < 99999 ) {printf "%.8f %.8f %.2f\n", $1,$2,$3}}' $chunk_name_full_clip"_tmp.xyz" > $chunk_name_full_clip".xyz"
		    echo -- Converted to xyz
		    rm $chunk_name_full_clip"_tmp.xyz" 
		    mv $chunk_name_full_clip tif_clip/$chunk_name_full_clip
		    mv $chunk_name_full_clip".xyz" xyz/$chunk_name_full_clip".xyz"
		fi
		

		yoff=$(echo "$yoff+$chunk_dim_y_int" | bc)
	    chunk_name=$((chunk_name+1))
	    done
	  xoff=$(echo "$xoff+$chunk_dim_x_int" | bc)
	done
	file_num=$((file_num + 1))
	echo
	echo
done

else
	help
fi

