#NOTE: HAVENT IMPLEMENTED THIS SCRIPT YET

mkdir -p unzipped
mkdir -p tif
mkdir -p xyz

study_area_buff_outer_shp=$1
bs_dlist=$2
dem_dlist=$3

for i in *.tif
do
#Clip data the study area buff ring
#Chunk the tifs and convert to xyz
  echo "Converting tif to xyz"
  gdal_translate -of XYZ $i $i"_tmp".xyz
  awk '{if ($3 > -999999 && $3 < 999999 ) {printf "%.8f %.8f %.2f\n", $1,$2,$3}}' $i"_tmp".xyz > xyz/$i.xyz
  rm $i"_tmp".xyz
done

cd xyz
./create_datalist.sh grids_ncei
echo "$PWD/grids_ncei.datalist -1 1" >> $bs_dlist
echo "$PWD/grids_ncei.datalist -1 1" >> $dem_dlist
