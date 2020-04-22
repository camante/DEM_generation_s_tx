'''
Description:
-Download lidar by clipping digital coast index shp to study area poly
-Some datasets don't work with fetch. Need to download manually?
-Clip superceded datasets with Matt's ogr?
-Convert to xyz
-Separate topo and topo bathy.
-Separate topobathy into pos and neg. Neg goes into bathy surface.

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

# if not os.path.exists('dc_lidar'):
# 	os.makedirs('dc_lidar')

main_dir=sys.argv[1]
basename=sys.argv[2]
data_url=sys.argv[3]
roi_shp=sys.argv[4]

#other params
dc_lidar_download_process='dc_lidar_download_process.csv'

#os.chdir('dc_lidar')
print 'Downloading lidar from Digital Coast'

dc_lidar_download_cmd='download_process_lidar.sh ' + main_dir + ' ' + basename + ' ' + data_url + ' ' + roi_shp
os.system(dc_lidar_download_cmd)

#Download any datasets with bad digital coast index.shp



