'''
Description:
-Download missing lidar
-manually download missing lidar datasets
-manually edit index shp to have only laz tiles desired
-download laz
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
######################## NOS ####################################
print "Current directory is ", os.getcwd()

#manually downloaded lidar-derived DEM that didn't have laz files using digital coast
#E:\COASTAL_Act\camante\w_fl\data\dc_lidar\missing\2007_FDEM_Southwest
#tif2chunks2xyz.sh 500 no 0.0000102880663
#below is from AL/FL DEMs


# main_dir=sys.argv[1]
# #main_dir='/media/sf_external_hd/al_fl'

# #other params
# dc_lidar_missing='dc_lidar_missing_download_process.csv'

# print 'Downloading lidar from Digital Coast'

# dc_lidar_missing_download_cmd='download_process_missing_lidar.sh ' + main_dir + ' ' + main_dir + '/data/' + dc_lidar_missing
# os.system(dc_lidar_missing_download_cmd)

# print "Downloading SLR DEM to fill in gaps without lidar"

# #Download OCM SLR Viewer DEM to fill in areas where I can't get raw data
# os.system('cd')

# #manually download SLR Viewer DEM from DAV and put in folder below
# os.chdir(main_dir+'/data/dc_lidar/missing/slr_dem')

# print "Converting SLR DEM to chunks and xyz"
# #Convert tif to xyz
# os.system('tif2chunks2xyz.sh 500 yes 0.000030864199')

# #create datalist
# print "Creating Datalist"
# os.chdir('xyz')
# os.system('create_datalist.sh slr_dem')

# #add datalist to master
# print "Added Datalist to Master Datalist"
# current_dir=os.getcwd()
# add_to_master_cmd='echo ' + current_dir + '/slr_dem.datalist -1 0.00001 >> ' + main_dir + '/software/gridding/al_fl.datalist' 
# #echo "/media/sf_external_hd/al_fl/data/dc_lidar/missing/slr_dem/xyz/slr_dem.datalist -1 0.00001" >> /media/sf_external_hd/al_fl/software/gridding/al_fl.datalist
# os.system(add_to_master_cmd)



