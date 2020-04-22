'''
Description:
-Manually Download ENCs SoundingsP at each scale (approach, harbour) via https://encdirect.noaa.gov/
-don't use overview, general, coastal, berthing scales.
-unzip folders
-move shp to same directory
-convert to xyz, negative
-convert mllw to navd88
-create_datalist

Author:
Chris Amante
Christopher.Amante@colorado.edu

Date:
1/14/2020

'''
#################################################################
#################################################################
#################################################################
####################### IMPORT MODULES ##########################
#################################################################
#################################################################
#################################################################
import os
import sys
######################## ENC ####################################
print "Current directory is ", os.getcwd()

if not os.path.exists('shp'):
	os.makedirs('shp')

if not os.path.exists('xyz'):
	os.makedirs('xyz')

main_dir=sys.argv[1]
conv_grd_path=sys.argv[2]
bs_dlist=sys.argv[3]

print "Already Manually download ENCs SoundingsP"

print "Unzipping folders"
os.system('unzip "*.zip"')

print "Moving all shp files to shp directory"
move_shp_cmd="find . -name '*.shp' -exec mv {} shp/ \; 2>/dev/null"
os.system(move_shp_cmd)
move_shx_cmd="find . -name '*.shx' -exec mv {} shp/ \; 2>/dev/null"
os.system(move_shx_cmd)
move_prj_cmd="find . -name '*.prj' -exec mv {} shp/ \; 2>/dev/null"
os.system(move_prj_cmd)
move_dbf_cmd="find . -name '*.dbf' -exec mv {} shp/ \; 2>/dev/null"
os.system(move_dbf_cmd)

print "Converting ENC to X,Y,Negative Z"
os.chdir('shp')
shp2xyz=('enc_shp2xyz.sh')
os.system(shp2xyz)

os.chdir('..')

print "Moving all xyz files to xyz directory"
move_xyz_cmd="find . -name '*.xyz' -exec mv {} xyz/ \; 2>/dev/null"
os.system(move_xyz_cmd)

print "Converting ENC to NAVD88"
os.chdir('xyz')
enc2navd88_cmd="vert_conv.sh " + conv_grd_path + "  navd88"
os.system(enc2navd88_cmd)

print "Creating ENC Datalist"
os.chdir('navd88')
enc_datalist_cmd='create_datalist.sh enc'
os.system(enc_datalist_cmd)

current_dir=os.getcwd()
add_to_bmaster_cmd='echo ' + current_dir + '/enc.datalist -1 0.0001 >> ' + bs_dlist
os.system(add_to_bmaster_cmd)
