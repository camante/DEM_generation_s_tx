'''
Description:
-Download lidar not on digital (i.e., NationalMap)
-Convert to xyz

Author:
Chris Amante
Christopher.Amante@colorado.edu

Date:
6/5/2019

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
######################## TOPO ####################################
#main_dir=sys.argv[1]
main_dir='/media/sf_external_hd/al_fl'

# print "Current directory is ", os.getcwd()

# if not os.path.exists('topo'):
# 	os.makedirs('topo')

# if not os.path.exists('topo/2007_app_river_fl'):
# 	os.makedirs('topo/2007_app_river_fl')

# os.chdir('topo/2007_app_river_fl)

# os.chdir('xyz')

# print 'Downloading lidar from the NationalMap'
# topo_download_cmd='wget -c -nc -np -r -nH -L --cut-dirs=8 ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/FL_Apalachicola_River_Area_2007/laz/'
# os.system(topo_download_cmd)

# print "Processing Laz to XYZ"
# laz2xyz_cmd='laz2xyz_repro.sh 2 26916 feet meter'
# os.system(laz2xyz_cmd)

# print "Creating Datalist"
# create_datalist_cmd='create_datalist.sh 2007_app_river_fl'
# os.system(create_datalist_cmd)

# print "Added Datalist to Master Datalist"
# current_dir=os.getcwd()
# add_to_master_cmd='echo ' + current_dir + '/2007_app_river_fl.datalist -1 1 >> ' + main_dir + '/software/gridding/al_fl.datalist' 
# os.system(add_to_master_cmd)

if not os.path.exists('topo/coned'):
	os.makedirs('topo/coned')

os.chdir('topo/coned')
#Manually download from https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/topo/downloads/Topobathy/TOPOBATHY_MOBILE_BAY_ELEV_METERS.zip
#unzipped, and renamed to usgs_mobile.tif

#Tile
os.system('tif2chunks_clip_2xyz.sh 500 no 0.000030864199 al_fl_coast_coned yes')


print "Creating Datalist"
os.chdir('xyz')
create_datalist_cmd='create_datalist.sh coned_mobile_2013'
os.system(create_datalist_cmd)

print "Added Datalist to Master Datalist"
current_dir=os.getcwd()
add_to_master_cmd='echo ' + current_dir + '/coned_mobile_2013.datalist -1 0.001 >> ' + main_dir + '/software/gridding/al_fl.datalist' 
#echo "/media/sf_external_hd/al_fl/data/topo/coned/xyz/coned_mobile_2013.datalist -1 0.001" >> /media/sf_external_hd/al_fl/software/gridding/al_fl.datalist
os.system(add_to_master_cmd)


#need to change dir

if not os.path.exists('topo/ncei'):
	os.makedirs('topo/ncei')

os.chdir('topo/ncei')
os.system('tif2chunks_clip_2xyz.sh 500 yes 0.000030864199 al_fl_coast_ncei yes')

print "Creating Datalist"
os.chdir('xyz')
create_datalist_cmd='create_datalist.sh ncei_mobile_2009'
os.system(create_datalist_cmd)

print "Added Datalist to Master Datalist"
current_dir=os.getcwd()
add_to_master_cmd='echo ' + current_dir + '/ncei_mobile_2009.datalist -1 0.0001 >> ' + main_dir + '/software/gridding/al_fl.datalist' 
#echo "/media/sf_external_hd/al_fl/data/topo/ncei/xyz/ncei_mobile_2009.datalist -1 0.0001" >> /media/sf_external_hd/al_fl/software/gridding/al_fl.datalist
os.system(add_to_master_cmd)


#need to change dir

if not os.path.exists('topo/ned'):
	os.makedirs('topo/ned')

os.chdir('topo/ned')
# Manually downloaded from National Map, but could do programatically here
os.system('tif2chunks_clip_2xyz.sh 500 yes 0.000030864199 al_fl_coast_ned yes')

print "Creating Datalist"
os.chdir('xyz')
create_datalist_cmd='create_datalist.sh ned'
os.system(create_datalist_cmd)

print "Added Datalist to Master Datalist"
current_dir=os.getcwd()
add_to_master_cmd='echo ' + current_dir + '/ned.datalist -1 0.00001 >> ' + main_dir + '/software/gridding/al_fl.datalist' 
#echo "/media/sf_external_hd/al_fl/data/topo/ned/xyz/ned.datalist -1 0.00001" >> /media/sf_external_hd/al_fl/software/gridding/al_fl.datalist
os.system(add_to_master_cmd)


