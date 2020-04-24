#!/bin/bash
function help () {
echo "download_mb_roi.sh - A script that downloads mb data in chunks from a WESN ROI, runs blockmedian, and then converts to xyz."
    echo "Usage: $0 name_cell_extents cellsize"
    echo "* name_cell_extents: <csv with names, cellsize, and extents>"
    echo "* cellsize: <blockmedian cell size in arc-seconds>
    0.000092592596 = 1/3rd arc-second
    0.00027777777 = 1 arc-second"
}


if [ ${#@} == 2 ]; 
then
roi_str_gmt=$1
bm_cell=$2

echo "roi str gmt is" $roi_str_gmt
echo "bm cellsize is" $bm_cell

mkdir -p xyz
echo "downloading all fbt files in study area ROI"
fetches mb -R $roi_str_gmt

echo "Moving all fbt files to chunk directory"
find . -name '*.fbt' -mindepth 2 -exec mv -i -- {} . \;

echo "Converting fbt to xyz"
for i in *.fbt;
do
	echo "Working on file" $i
	echo "Converting to XYZ"
	mblist -MX20 -OXYZ -I$i -R$roi_str_gmt | awk '{printf "%.8f %.8f %.3f\n", $1,$2,$3}' > $(basename $i .fbt)".xyz"
	echo "Running blockmedian"
	gmt blockmedian $(basename $i .fbt)".xyz" -I$bm_cell/$bm_cell -R$roi_str_gmt -V -Q > $(basename $i .fbt)"_bm_tmp.xyz"
	awk '{printf "%.8f %.8f %.2f\n", $1,$2,$3}' $(basename $i .fbt)"_bm_tmp.xyz" > xyz/$(basename $i .fbt)"_bm.xyz"
	rm $(basename $i .fbt)".xyz"
	rm $(basename $i .fbt)"_bm_tmp.xyz"
echo
echo
done

echo "moving all xyz files to the same directory"
find . -name '*.xyz' -exec mv {} xyz/ \; 2>/dev/null

echo "deleting all fbt files"
rm *.fbt

else
    help
fi

#for i in */; do echo $i; cd $i; mkdir xyz; for j in *.*; do mblist -R-92.255/-88.495/28.495/31.005 -MX20 -OXYZ -I$j > xyz/$j.xyz; done; cd ..; done
