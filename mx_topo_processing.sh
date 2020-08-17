mkdir -p unzipped
mkdir -p tif
mkdir -p xyz

mx_clip_shp=$1
dem_dlist=$2

for zip_file in *.zip
do
  echo "processing zip file" $zip_file
  zip_dir_name=$(basename -s .zip $zip_file)
  mkdir -p $zip_dir_name
  echo "zip dir name is " $zip_dir_name
  unzip -o $zip_file -d $zip_dir_name
  cd $zip_dir_name
  cd MT_Grid
  cd *
  sub_dir=$(pwd)
  arc_grid="$(ls -d *_mt)"
  echo "arc_grid name is" $arc_grid
  echo "Reprojecting arc_grid to nad83.tif"
  gdalwarp -r cubicspline -dstnodata -999999 -s_srs EPSG:26914 -t_srs EPSG:4269 -of GTiff $arc_grid $arc_grid".tif"
  echo "copying shp to current dir"
  cp ../../../$mx_clip_shp".shp" $mx_clip_shp".shp"
  cp ../../../$mx_clip_shp".dbf" $mx_clip_shp".dbf"
  cp ../../../$mx_clip_shp".shx" $mx_clip_shp".shx"
  cp ../../../$mx_clip_shp".prj" $mx_clip_shp".prj"
  echo "Clipping to shp"
  gdal_rasterize -burn -999999 -i -l $mx_clip_shp $mx_clip_shp".shp" $arc_grid".tif"
  rm $mx_clip_shp".shp"
  rm $mx_clip_shp".dbf"
  rm $mx_clip_shp".shx"
  rm $mx_clip_shp".prj"
  echo "Converting clipped tif to xyz"
  gdal_translate -of XYZ $arc_grid.tif $arc_grid"_tmp".xyz
  awk '{if ($3 > 0.000000 && $3 < 999999 ) {printf "%.8f %.8f %.2f\n", $1,$2,$3}}' $arc_grid"_tmp.xyz" > $arc_grid".xyz"
  rm $arc_grid"_tmp".xyz
  mv $arc_grid".xyz" ../../../xyz
  mv $arc_grid".tif" ../../../tif
  cd ..
  cd ..
  cd ..
  mv $zip_dir_name unzipped/$zip_dir_name
done

cd xyz
./create_datalist.sh mx_topo 
echo "$PWD/mx_topo.datalist -1 0.01" >> $dem_dlist
