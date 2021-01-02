sql_var=5186_clip_index_superceded
echo "Dropping all Columns but Name"
ogr2ogr -f "ESRI Shapefile" -sql "SELECT NAME FROM \"$sql_var\"" 5186_clip_index_superceded_name.shp 5186_clip_index_superceded.shp

echo "Converting SHP to CSV"
ogr2ogr -f CSV 5186_clip_index_superceded_name.csv 5186_clip_index_superceded_name.shp

echo "Removing Header and Quotes"
sed '1d' 5186_clip_index_superceded_name.csv > tmpfile; mv tmpfile 5186_clip_index_superceded_name.csv
sed 's/"//' 5186_clip_index_superceded_name.csv > tmpfile; mv tmpfile 5186_clip_index_superceded_name.csv

echo "Moving superceded files"
mkdir -p xyz/pos/superceded
mkdir -p xyz/neg/superceded
# Get URLs from csv
IFS=,
sed -n '/^ *[^#]/p' 5186_clip_index_superceded_name.csv |
while read -r line
do
laz_name=$(echo $line | awk '{print $1}')
echo "copying" $laz_name
mv xyz/pos/$(basename $laz_name .laz)"_class_2_pos.xyz" xyz/pos/superceded/$(basename $laz_name .laz)"_class_2_pos.xyz"        
mv xyz/pos/$(basename $laz_name .laz)"_class_29_pos.xyz" xyz/pos/superceded/$(basename $laz_name .laz)"_class_29_pos.xyz"
mv xyz/pos/$(basename $laz_name .laz)"_class_2_pos.xyz.inf" xyz/pos/superceded/$(basename $laz_name .laz)"_class_2_pos.xyz.inf"
mv xyz/pos/$(basename $laz_name .laz)"_class_29_pos.xyz.inf" xyz/pos/superceded/$(basename $laz_name .laz)"_class_29_pos.xyz.inf"
mv xyz/neg/$(basename $laz_name .laz)"_class_2_neg.xyz" xyz/neg/superceded/$(basename $laz_name .laz)"_class_2_neg.xyz"
mv xyz/neg/$(basename $laz_name .laz)"_class_29_neg.xyz" xyz/neg/superceded/$(basename $laz_name .laz)"_class_29_neg.xyz"
mv xyz/neg/$(basename $laz_name .laz)"_class_2_neg.xyz.inf" xyz/neg/superceded/$(basename $laz_name .laz)"_class_2_neg.xyz.inf"
mv xyz/neg/$(basename $laz_name .laz)"_class_29_neg.xyz.inf" xyz/neg/superceded/$(basename $laz_name .laz)"_class_29_neg.xyz.inf"
echo
done

cd xyz/pos/
./create_datalist.sh 5186_lidar_pos
cd ..
cd ..

cd xyz/neg/
./create_datalist.sh 5186_lidar_neg
