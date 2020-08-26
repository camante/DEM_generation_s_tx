#!/bin/bash
function help () {
echo "create_spatial_meta- Script that creates spatial metadata for multiple DEM tiles"
	echo "Usage: $0 name_cell_extents datalist sm_res year version"
	echo "* name_cell_extents: <csv file with name,target spatial resolution in decimal degrees,tile_exents in W,E,S,N>"
	echo "* datalist: <master datalist file that points to individual datasets datalists>"
	echo "* sm_res: <spatial metadata output resolution>
	0.00003086420 = 1/9th arc-second 
	0.00009259259 = 1/3rd arc-second
	0.00027777777 = 1 arc-second"
	echo "* year: <year of DEM generation>"
	echo "* version: <version of DEM tile>"
}

#see if 4 parameters were provided
#show help if not
if [ ${#@} == 5 ]; 
then
name_cell_extents=$1
datalist=$2
sm_res=$3
year=$4
version=$5

# Get Tile Name, Cellsize, and Extents from name_cell_extents.csv
IFS=,
sed -n '/^ *[^#]/p' $name_cell_extents |
while read -r line
do
name=$(echo $line | awk '{print $1}')
target_res=$(echo $line | awk '{print $2}')
west_quarter=$(echo $line | awk '{print $3}')
east_quarter=$(echo $line | awk '{print $4}')
south_quarter=$(echo $line | awk '{print $5}')
north_quarter=$(echo $line | awk '{print $6}')

echo
echo "Tile Name is" $name
echo "West is" $west_quarter
echo "East is" $east_quarter
echo "South is" $south_quarter
echo "North is" $north_quarter
echo

# #Expand DEM extents by 6 cells to provide overlap between tiles
# #Dont need to do anymore with Matt's extend switch

# six_cells_target=$(echo "$target_res * 6" | bc -l)
# #echo six_cells_target is $six_cells_target
# west=$(echo "$west_quarter - $six_cells_target" | bc -l)
# north=$(echo "$north_quarter + $six_cells_target" | bc -l)
# east=$(echo "$east_quarter + $six_cells_target" | bc -l)
# south=$(echo "$south_quarter - $six_cells_target " | bc -l)

#get final name

north_degree=${north_quarter:0:2}
north_decimal=${north_quarter:3:2}

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

west_degree=${west_quarter:1:2}
west_decimal=${west_quarter:4:2}

if [ -z "$west_decimal" ]
then
	west_decimal="00"
else
	:
fi

size=${#west_decimal}
if [ "$size" = 1 ]
then
	west_decimal="$west_decimal"0
else
	:
fi

echo

if [ "$cellsize_degrees" = 0.00003086420 ]
then
	cell_name=19
else
	cell_name=13
fi



#old extend method
#echo waffles -R $west"/"$east"/"$south"/"$north -E $sm_res -V -O ncei$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_"$year"v"$version -M datalists -s $datalist -P 4269
#echo
#waffles -R $west"/"$east"/"$south"/"$north -E $sm_res -V -O ncei$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_"$year"v"$version -M datalists -s $datalist -P 4269 

echo waffles -R $west_quarter"/"$east_quarter"/"$south_quarter"/"$north_quarter -E $sm_res -V -O ncei$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_"$year"v"$version -M datalists -s $datalist -P 4269 -X6:12
echo
waffles -R $west_quarter"/"$east_quarter"/"$south_quarter"/"$north_quarter -E $sm_res -V -O ncei$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_"$year"v"$version -M datalists -s $datalist -P 4269 -X6:12

echo
echo waffles -R $west_quarter"/"$east_quarter"/"$south_quarter"/"$north_quarter -E $sm_res -V -O ncei$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_"$year"v"$version -M datalists -s $datalist -P 4269 -X6:12
echo
echo "Completed spatial metadata generation for " $name
echo "ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_"$year"v"$version
echo
echo
done

else
	help
fi
