#!/bin/bash
function help () {
echo "download_mb_tiles.sh - A script that downloads mb data in DEM tiles, runs blockmedian, and then converts to xyz."
    echo "Usage: $0 name_cell_extents cellsize"
    echo "* name_cell_extents: <csv with names, cellsize, and extents>"
    echo "* cellsize: <blockmedian cell size in arc-seconds>
    0.000092592596 = 1/3rd arc-second
    0.00027777777 = 1 arc-second"
}


if [ ${#@} == 2 ]; 
then

tile_extents=$1
blkmed_cell=$2

mkdir -p xyz

# Get Tile Name, Cellsize, and Extents from name_cell_extents.csv
IFS=,
sed -n '/^ *[^#]/p' $tile_extents |
while read -r line
do
tile_name=$(echo $line | awk '{print $1}')
cellsize_degrees=$(echo $line | awk '{print $2}')
west_quarter=$(echo $line | awk '{print $3}')
east_quarter=$(echo $line | awk '{print $4}')
south_quarter=$(echo $line | awk '{print $5}')
north_quarter=$(echo $line | awk '{print $6}')

echo "Tile Name is" $tile_name
echo "Cellsize in degrees is" $cellsize_degrees
echo "West is" $west_quarter
echo "East is" $east_quarter
echo "South is" $south_quarter
echo "North is" $north_quarter

#############################################################################
#############################################################################
#############################################################################
######################      DERIVED VARIABLES     ###########################
#############################################################################
#############################################################################
#############################################################################

six_cells_target=$(echo "$cellsize_degrees * 6" | bc -l)

west=$(echo "$west_quarter - $six_cells_target" | bc -l)
north=$(echo "$north_quarter + $six_cells_target" | bc -l)
east=$(echo "$east_quarter + $six_cells_target" | bc -l)
south=$(echo "$south_quarter - $six_cells_target " | bc -l)

#Take in a half-cell on all sides so that grid-registered raster edge aligns exactly on desired extent
half_cell=$(echo "$cellsize_degrees / 2" | bc -l)
echo half_cell is $half_cell
west_reduced=$(echo "$west + $half_cell" | bc -l)
north_reduced=$(echo "$north - $half_cell" | bc -l)
east_reduced=$(echo "$east - $half_cell" | bc -l)
south_reduced=$(echo "$south + $half_cell" | bc -l)

echo "West_reduced is" $west_reduced
echo "East_reduced is" $east_reduced
echo "South_reduced is" $south_reduced
echo "North_reduced is" $north_reduced

#Determine number of rows and columns with the desired cell size, rounding up to nearest integer.
#i.e., 1_9 arc-second
x_diff=$(echo "$east - $west" | bc -l)
y_diff=$(echo "$north - $south" | bc -l)
x_dim=$(echo "$x_diff / $cellsize_degrees" | bc -l)
y_dim=$(echo "$y_diff / $cellsize_degrees" | bc -l)
x_dim_int=$(echo "($x_dim+0.5)/1" | bc)
y_dim_int=$(echo "($y_dim+0.5)/1" | bc)
buffer=$(echo "($x_dim_int+0.5)/20" | bc)
buffer_cell=$(echo "($buffer*$cellsize_degrees)" | bc -l)
echo "x dims:" $x_dim_int
echo "y dims:" $y_dim_int
echo "buffer:" $buffer
echo "buffer in cells:" $buffer_cell

#Extend each grid by ~5% to have data buffer.
west_buffer=$(echo "$west - $buffer_cell" | bc -l)
north_buffer=$(echo "$north + $buffer_cell" | bc -l)
east_buffer=$(echo "$east + $buffer_cell" | bc -l)
south_buffer=$(echo "$south - $buffer_cell" | bc -l)

echo "West_buffer is" $west_buffer
echo "East_buffer is" $east_buffer
echo "South_buffer is" $south_buffer
echo "North_buffer is" $north_buffer

# Do processing here
echo Downloading MB Data
mkdir -p $tile_name
cd $tile_name

echo $mb_range
fetches mb -R $west_buffer/$east_buffer/$south_buffer/$north_buffer

echo "Moving all fbt files to tile directory"
find . -name '*.fbt' -mindepth 2 -exec mv -i -- {} . \;

echo "Converting fbt to xyz"
for i in *.fbt;
do
	echo "Working on file" $i
	echo "Converting to XYZ"
	mblist -MX20 -OXYZ -I$i -R$west_buffer/$east_buffer/$south_buffer/$north_buffer | awk '{printf "%.8f %.8f %.3f\n", $1,$2,$3}' > $tile_name"_"$(basename $i .fbt)".xyz"
	echo "Running blockmedian"
	gmt blockmedian $tile_name"_"$(basename $i .fbt)".xyz" -I$blkmed_cell/$blkmed_cell -R$west_buffer/$east_buffer/$south_buffer/$north_buffer -V -Q > $tile_name"_"$(basename $i .fbt)"_bm_tmp.xyz"
	awk '{printf "%.8f %.8f %.2f\n", $1,$2,$3}' $tile_name"_"$(basename $i .fbt)"_bm_tmp.xyz" > $tile_name"_"$(basename $i .fbt)"_bm.xyz"
	rm $tile_name"_"$(basename $i .fbt)"_bm_tmp.xyz"
	rm $tile_name"_"$(basename $i .fbt)".xyz"
echo
echo
done
cd ..
done

echo "moving all xyz files to the same directory"
find . -name '*.xyz' -exec mv {} xyz/ \; 2>/dev/null

else
    help
fi

#for i in */; do echo $i; cd $i; mkdir xyz; for j in *.*; do mblist -R-92.255/-88.495/28.495/31.005 -MX20 -OXYZ -I$j > xyz/$j.xyz; done; cd ..; done
