for i in *.shp
do
echo Processing $i
xyz_name=$(basename $i .shp)
echo name is $xyz_name
ogr2ogr -f CSV $i"_tmp.csv" $i -lco GEOMETRY=AS_WKT
sed -e 's/\(^.*(\)\(.*\)\().*$\)/\2/' $i"_tmp.csv" > $xyz_name"_tmp.xyz"
awk 'FNR>1{printf "%.8f %.8f %.3f\n", $1,$2,$3*-1}' $xyz_name"_tmp.xyz" > $xyz_name"_neg_m.xyz"
rm $xyz_name"_tmp.xyz"
rm $i"_tmp.csv"
echo 
echo
done


