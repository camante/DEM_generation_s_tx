#!/usr/bin/python

'''
Description:
Master Script to Generate DEMs for S TX. 

Author:
Christopher Amante
Christopher.Amante@colorado.edu

Date:
4/22/2020

'''
#################################################################
#################################################################
#################################################################
####################### IMPORT MODULES ##########################
#################################################################
#################################################################
#################################################################
import os
import subprocess
import sys
import glob
#################################################################
#################################################################
#################################################################
###################### INITIAL VARIABLES ########################
#################################################################
#################################################################
#################################################################
basename="s_tx"
main_dir='/media/sf_E_win_lx/COASTAL_Act/camante/s_tx'
data_dir=main_dir+'/data'
docs_dir=main_dir+'/docs'
software_dir=main_dir+'/software'
code_dir=main_dir+'/code/DEM_generation'+'_'+basename
#
#

conv_grd_path=data_dir+'/conv_grd/cgrid_mllw2navd88.tif'
name_cell_extents_bs=data_dir+'/bathy/bathy_surf/name_cell_extents_bs.csv'
name_cell_extents_dem=software_dir+'/gridding/name_cell_extents_dem.csv'
name_cell_extents_dem_all=software_dir+'/gridding/name_cell_extents_dem_all.csv'
bs_dlist=data_dir+'/bathy/bathy_surf/s_tx_bs.datalist'
dem_dlist=software_dir+'/gridding/s_tx_dem.datalist'
bs_path=data_dir+'/bathy/bathy_surf/tifs'
coast_shp=data_dir+'/coast/'+basename+'_coast'
dc_lidar_download_process=data_dir+'/dc_lidar_download_process.csv'
#shp for data download
study_area_shp=main_dir+'/data/study_area/'+basename+'_tiles_buff.shp'

#Creating main subdirectories
dir_list=[data_dir, docs_dir, software_dir, software_dir+'/gridding']
for i in dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#Create Empty Dummy BS, Bathy Surface and DEM datalists
create_bs_dlist='''if [ ! -e {}/bathy/bathy_surf/s_tx_bs.datalist ] ; 
then touch {}/bathy/bathy_surf/{}_bs.datalist
fi'''.format(data_dir,data_dir,basename)
os.system(create_bs_dlist)

create_dem_dlist='''if [ ! -e {}/gridding/s_tx_dem.datalist ] ; 
then touch {}/gridding/{}_dem.datalist
fi'''.format(software_dir,software_dir,basename)
os.system(create_dem_dlist)

#ROI for data download
west_buff=-98.05
east_buff=-96.45
south_buff=25.70
north_buff=29.05
roi_str_gmt=str(west_buff)+'/'+str(east_buff)+'/'+str(south_buff)+'/'+str(north_buff)
roi_str_ogr=str(west_buff)+' '+str(south_buff)+' '+str(east_buff)+' '+str(north_buff)

#test_ROI
#roi_str_gmt='-98.05/-96.45/25.7/29.05'
#roi_str_ogr='-98.05 25.7 -96.45 29.05'

#small mb test
# west_buff=-97.5
# east_buff=-97.25
# south_buff=27.75
# north_buff=28.0
# roi_str_gmt=str(west_buff)+'/'+str(east_buff)+'/'+str(south_buff)+'/'+str(north_buff)

print "ROI is", roi_str_gmt
print "ROI OGR is", roi_str_ogr
#sys.exit()

#################################################################
#################################################################
#################################################################
####################### PRE-PROCESSING ##########################
#################################################################
#################################################################
#################################################################
# #Create Conversion Grid -- MLLW to NAVD88
# if not os.path.exists('data/conv_grd'):
# 	os.makedirs('data/conv_grd')

# os.chdir(data_dir+'/conv_grd')
# print "Creating mllw2navd88 conversion grid"
# #conv_grd_cmd='waffles conversion-grid:mllw:navd88 -E1s -R{} -I{}'.format(roi_str_gmt, bs_dlist)
# conv_grd_cmd='waffles --verbose -R{} -E1s -O cgrid_mllw2navd88.tif vdatum:ivert=mllw:overt=navd88'.format(roi_str_gmt)
# #waffles -R-98.05/-96.45/25.7/29.05 -E1s -O cgrid_mllw2navd88.tif vdatum:ivert=mllw:overt=navd88
# print conv_grd_cmd
# #sys.exit()
# os.system(conv_grd_cmd)
# DONE

#################################################################
#################################################################
#################################################################
####################### DATA DOWNLOAD ###########################
#################################################################
#################################################################
#################################################################

#################################################################
####################### STUDY AREA ##############################
#################################################################
#manually created shp in ArcGIS (s_tx_tiles.shp) 
#created name_cell_extents with arcpy get_poly_coords.py (name_cell_extents_bs.csv; name_cell_extents_DEM.csv) 
#manually created study area buffer in ArcMap (s_tx_tiles_buff.shp)

# #################################################################
# ######################## COASTLINE ##############################
# #################################################################
# os.chdir(data_dir)
# print 'Current Directory is', os.getcwd()

# coast_dir_list=['coast']
# for i in coast_dir_list:
# 	if not os.path.exists(i):
# 		print 'creating subdir', i
# 		os.makedirs(i)

# os.chdir(coast_dir_list[0])

# # #delete python script if it exists
# os.system('[ -e coast_processing.py ] && rm coast_processing.py')
# # #copy python script from DEM_generation code

# os.system('cp {}/coast_processing.py coast_processing.py'.format(code_dir)) 

# print "executing coast_processing script"
# os.system('python coast_processing.py {} {} {} {} {}'.format(basename,main_dir,study_area_shp,roi_str_ogr,roi_str_gmt))

# #################################################################
# ########################## BATHY ################################
# #################################################################
os.chdir(data_dir+'/bathy')
print 'Current Directory is', os.getcwd()

#Creating main subdirectories
bathy_dir_list=['usace_dredge', 'mb', 'nos', 'enc']
for i in bathy_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

# ####################### USACE DREDGE #############################
# os.chdir(bathy_dir_list[0])
# print 'Current Directory is', os.getcwd()

######## CODE MANAGEMENT #########
# #delete python script if it exists
# os.system('[ -e usace_dredge_processing.py ] && rm usace_dredge_processing.py')
# #copy python script from DEM_generation code
# os.system('cp {}/usace_dredge_processing.py usace_dredge_processing.py'.format(code_dir)) 

# #delete shell script if it exists
# os.system('[ -e csv/usace_ft2m.sh ] && rm csv/usace_ft2m.sh')
# #copy sh script from DEM_generation code
# os.system('cp {}/usace_ft2m.sh csv/usace_ft2m.sh'.format(code_dir)) 

# #delete shell script if it exists
# os.system('[ -e xyz/vert_conv.sh ] && rm xyz/vert_conv.sh')
# #copy sh script from DEM_generation code
# os.system('cp {}/vert_conv.sh xyz/vert_conv.sh'.format(code_dir)) 

# #delete shell script if it exists
# os.system('[ -e xyz/navd88/create_datalist.sh ] && rm xyz/navd88/create_datalist.sh')
# #copy sh script from DEM_generation code
# os.system('cp {}/create_datalist.sh xyz/navd88/create_datalist.sh'.format(code_dir)) 
######## CODE MANAGEMENT #########

# print "executing usace_dredge_processing script"
# os.system('python usace_dredge_processing.py {} {} {} {} {} {} {}'.format(main_dir, code_dir, study_area_shp, roi_str_gmt, conv_grd_path, bs_dlist, dem_dlist))

# ######################## Multibeam #############################
os.system('cd')
os.chdir(main_dir+'/data/bathy')
os.chdir(bathy_dir_list[1])
print 'Current Directory is', os.getcwd()

os.system('mkdir -p xyz')

######## CODE MANAGEMENT #########
#delete python script if it exists
os.system('[ -e mb_processing.py ] && rm mb_processing.py')
#copy python script from DEM_generation code
os.system('cp {}/mb_processing.py mb_processing.py'.format(code_dir))

#delete shell script if it exists
os.system('[ -e download_mb_roi.sh ] && rm download_mb_roi.sh')
#copy sh script from DEM_generation code
os.system('cp {}/download_mb_roi.sh download_mb_roi.sh'.format(code_dir)) 

#delete shell script if it exists
os.system('[ -e xyz/create_datalist.sh ] && rm xyz/create_datalist.sh')
#copy sh script from DEM_generation code
os.system('cp {}/create_datalist.sh xyz/create_datalist.sh'.format(code_dir)) 
######## CODE MANAGEMENT #########
#sys.exit()
print "executing mb_processing script"
os.system('python mb_processing.py {} {}'.format(roi_str_gmt, bs_dlist))
# ####
# ########################## NOS/BAG ################################
# os.system('cd')
# os.chdir(main_dir+'/data/bathy')
# os.chdir(bathy_dir_list[2])
# print 'Current Directory is', os.getcwd()

# #delete python script if it exists
# os.system('[ -e nos_processing.py ] && rm nos_processing.py')
# #copy python script from DEM_generation code
# os.system('cp {}/nos_processing.py nos_processing.py'.format(code_dir)) 

# print "executing nos_processing script"
# os.system('python nos_processing.py {} {} {} {} {}'.format(main_dir, roi_str_gmt, conv_grd_path, bs_dlist, dem_dlist))

# ########################## ENC ################################
# os.system('cd')
# os.chdir(main_dir+'/data/bathy')
# os.chdir(bathy_dir_list[3])
# print 'Current Directory is', os.getcwd()

# #delete python script if it exists
# os.system('[ -e enc_processing.py ] && rm enc_processing.py')
# #copy python script from DEM_generation code
# os.system('cp {}/enc_processing.py enc_processing.py'.format(code_dir)) 

# print "executing enc_processing script"
# os.system('python enc_processing.py {} {} {}'.format(main_dir, conv_grd_path, bs_dlist))

#############################################################
################## DIGITAL COAST LIDAR ######################
#############################################################
# os.system('cd')
# os.chdir(main_dir+'/data')

# dc_lidar_dir_list=['dc_lidar']
# for i in dc_lidar_dir_list:
# 	if not os.path.exists(i):
# 		print 'creating subdir', i
# 		os.makedirs(i)

# os.chdir(dc_lidar_dir_list[0])

# # #delete python script if it exists
# os.system('[ -e dc_lidar_processing.py ] && rm dc_lidar_processing.py')
# # #copy python script from DEM_generation code

# os.system('cp {}/dc_lidar_processing.py dc_lidar_processing.py'.format(code_dir)) 

# print "executing dc_lidar_processing script"
# os.system('python dc_lidar_processing.py {} {} {} {}'.format(main_dir,basename,dc_lidar_download_process,study_area_shp))


## manually downloaded lidar-derived DEM that didn't have laz files using digital coast
## E:\COASTAL_Act\camante\s_tx\data\dc_lidar\missing\2007_FDEM_Southwest
## tif2chunks2xyz.sh 500 no 0.0000102880663
## below is from AL/FL DEMs

# os.system('cd')
# os.chdir(main_dir+'/data/dc_lidar')

# dc_lidar_missing_dir_list=['missing']
# for i in dc_lidar_missing_dir_list:
# 	if not os.path.exists(i):
# 		print 'creating subdir', i
# 		os.makedirs(i)


# os.chdir(dc_lidar_missing_dir_list[0])

# # #delete python script if it exists
# os.system('[ -e dc_lidar_missing_processing.py ] && rm dc_lidar_missing_processing.py')
# # #copy python script from DEM_generation code

# os.system('cp {}/dc_lidar_missing_processing.py dc_lidar_missing_processing.py'.format(code_dir)) 

# print "executing dc_lidar_missing_processing script"
# os.system('python dc_lidar_missing_processing.py {}'.format(main_dir))


# #############################################################
# ################## TOPO NOT ON DIGITAL COAST ################
# #############################################################
# 
## Manually downloaded from USGS NED
## 

# # #################################################################
# # #################################################################
# # #################################################################
# # ####################### DATA PROCESSING #########################
# # #################################################################
# # #################################################################
# # #################################################################

# # #################################################################
# # #################################################################
# # #################################################################
# # ####################### BATHY SURFACE ###########################
# # #################################################################
# # #################################################################
# # #################################################################
# os.system('cd')
# os.chdir(main_dir+'/data/bathy')

# # Create Bathy Surface 
# if not os.path.exists('bathy_surf'):
#  	os.makedirs('bathy_surf')

# os.chdir('bathy_surf')
# bathy_surf_cmd='create_bs.sh ' + name_cell_extents_bs + ' ' + bs_dlist + ' ' + coast_shp
# os.system(bathy_surf_cmd)

# # # #################################################################
# # # #################################################################
# # # #################################################################
# # # ####################### DEM GENERATION ##########################
# # # #################################################################
# # # #################################################################
# # # #################################################################
# #Create DEM
# os.system('cd')
# os.chdir(main_dir)
# os.chdir('software/gridding')

# create_dem_cmd='create_dem.sh ' + name_cell_extents_dem + ' ' + dem_dlist + ' ' + str(5)
# #create_dem.sh /media/sf_E_win_lx/COASTAL_Act/camante/s_tx/software/gridding/name_cell_extents_dem.csv /media/sf_E_win_lx/COASTAL_Act/camante/s_tx/software/gridding/s_tx.datalist /media/sf_E_win_lx/COASTAL_Act/camante/s_tx/data/bathy/bathy_surf/tifs 5
# #create_dem.sh /media/sf_E_win_lx/COASTAL_Act/camante/s_tx/software/gridding/name_cell_extents_dem.csv /media/sf_E_win_lx/COASTAL_Act/camante/s_tx/software/gridding/s_tx.datalist 5
# os.system(create_dem_cmd)
