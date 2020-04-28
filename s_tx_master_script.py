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
###################### PROCESS VARIABLES ########################
#################################################################
#################################################################
#################################################################
conv_grd_process='no'
coast_process='no'
#bathy
usace_dredge_process='yes'
mb_process='yes'
nos_process='yes'
enc_process='no'

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
dir_list=[data_dir,	data_dir+'/conv_grd',docs_dir, software_dir, software_dir+'/gridding']
for i in dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#Creating main bathy subdirectories
os.chdir(data_dir+'/bathy')
bathy_dir_list=['usace_dredge', 'mb', 'nos', 'enc']
for i in bathy_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#Create Empty Bathy Surface and DEM Master datalists if they don't exist
create_bs_dlist='''if [ ! -e {}/bathy/bathy_surf/{}_bs.datalist ] ; 
then touch {}/bathy/bathy_surf/{}_bs.datalist
fi'''.format(data_dir,basename,data_dir,basename)
os.system(create_bs_dlist)

create_dem_dlist='''if [ ! -e {}/gridding/{}_dem.datalist ] ; 
then touch {}/gridding/{}_dem.datalist
fi'''.format(software_dir,basename,software_dir,basename)
os.system(create_dem_dlist)

#ROI for data download
west_buff=-98.05
east_buff=-96.45
south_buff=25.70
north_buff=29.05
roi_str_gmt=str(west_buff)+'/'+str(east_buff)+'/'+str(south_buff)+'/'+str(north_buff)
roi_str_ogr=str(west_buff)+' '+str(south_buff)+' '+str(east_buff)+' '+str(north_buff)

#small bathy download test
west_buff=-97.3
east_buff=-97.29
south_buff=27.79
north_buff=28.0
roi_str_gmt=str(west_buff)+'/'+str(east_buff)+'/'+str(south_buff)+'/'+str(north_buff)
roi_str_ogr=str(west_buff)+' '+str(south_buff)+' '+str(east_buff)+' '+str(north_buff)

#test_ROI
#roi_str_gmt='-98.05/-96.45/25.7/29.05'
#roi_str_ogr='-98.05 25.7 -96.45 29.05'

print "ROI is", roi_str_gmt
print "ROI OGR is", roi_str_ogr
#sys.exit()

#################################################################
#################################################################
#################################################################
####################### CONVERSION GRID #########################
#################################################################
#################################################################
#################################################################
#Create Conversion Grid -- MLLW to NAVD88
if conv_grd_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/conv_grd')
	print "Creating mllw2navd88 conversion grid"
	conv_grd_cmd='waffles --verbose -R {} -E 1s -O cgrid_mllw2navd88.tif vdatum:ivert=mllw:overt=navd88:region=3'.format(roi_str_gmt)
	print conv_grd_cmd
	os.system(conv_grd_cmd)
else:
	print "Skipping Conversion Grid Processing"

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
if coast_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/coast')
	print 'Current Directory is', os.getcwd()

	coast_dir_list=['coast']
	for i in coast_dir_list:
		if not os.path.exists(i):
			print 'creating subdir', i
			os.makedirs(i)
	os.chdir(coast_dir_list[0])

	####### CODE MANAGEMENT #########
	os.system('mkdir -p landsat')
	os.system('mkdir -p mx')
	os.system('mkdir -p nhd')
	os.system('mkdir -p nhd/zip')
	os.system('mkdir -p nhd/gdb')
	os.system('mkdir -p nhd/shp')
	os.system('mkdir -p nhd/shp/merge')

	#delete python script if it exists
	os.system('[ -e coast_processing.py ] && rm coast_processing.py')
	# copy python script from DEM_generation code
	os.system('cp {}/coast_processing.py coast_processing.py'.format(code_dir)) 

	print "executing coast_processing script"
	os.system('python coast_processing.py {} {} {} {} {}'.format(basename,main_dir,study_area_shp,roi_str_ogr,roi_str_gmt))
else:
	print "Skipping Coastline Processing"

# #################################################################
# ########################## BATHY ################################
# #################################################################
#usace_dredge,mb,nos,enc
# ####################### USACE DREDGE #############################
if usace_dredge_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/bathy/usace_dredge')
	print 'Current Directory is', os.getcwd()
	
	####### CODE MANAGEMENT #########
	os.system('mkdir -p zip')
	os.system('mkdir -p gdb')
	os.system('mkdir -p csv')
	os.system('mkdir -p xyz')
	os.system('mkdir -p xyz/navd88')

	#delete python script if it exists
	os.system('[ -e usace_dredge_processing.py ] && rm usace_dredge_processing.py')
	#copy python script from DEM_generation code
	os.system('cp {}/usace_dredge_processing.py usace_dredge_processing.py'.format(code_dir)) 

	#delete shell script if it exists
	os.system('[ -e csv/usace_ft2m.sh ] && rm csv/usace_ft2m.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/usace_ft2m.sh csv/usace_ft2m.sh'.format(code_dir)) 

	#delete shell script if it exists
	os.system('[ -e xyz/vert_conv.sh ] && rm xyz/vert_conv.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/vert_conv.sh xyz/vert_conv.sh'.format(code_dir)) 

	#delete shell script if it exists
	os.system('[ -e xyz/gdal_query.py ] && rm xyz/gdal_query.py')
	#copy sh script from DEM_generation code
	os.system('cp {}/gdal_query.py xyz/gdal_query.py'.format(code_dir)) 

	#delete shell script if it exists
	os.system('[ -e xyz/navd88/create_datalist.sh ] && rm xyz/navd88/create_datalist.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/create_datalist.sh xyz/navd88/create_datalist.sh'.format(code_dir)) 

	print "executing usace_dredge_processing script"
	os.system('python usace_dredge_processing.py {} {} {} {}'.format(roi_str_gmt, conv_grd_path, bs_dlist, dem_dlist))
else:
	print "Skipping USACE Dredge Processing"
######################### Multibeam #############################
if mb_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/bathy/mb')
	print 'Current Directory is', os.getcwd()
	
	######### CODE MANAGEMENT #########
	os.system('mkdir -p xyz')
	
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
	####
else:
	print "Skipping MB Processing"
# ########################## NOS/BAG ################################
if nos_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/bathy/nos')
	print 'Current Directory is', os.getcwd()
	
	######### CODE MANAGEMENT #########
	os.system('mkdir -p nos_hydro')
	os.system('mkdir -p nos_hydro/xyz')
	os.system('mkdir -p nos_hydro/xyz/neg_m')
	os.system('mkdir -p nos_hydro/xyz/neg_m/navd88')
	os.system('mkdir -p nos_bag')
	os.system('mkdir -p nos_bag/xyz')
	os.system('mkdir -p nos_bag/xyz/navd88')

	#delete python script if it exists
	os.system('[ -e nos_processing.py ] && rm nos_processing.py')
	#copy python script from DEM_generation code
	os.system('cp {}/nos_processing.py nos_processing.py'.format(code_dir)) 

	#NOS HYDRO
	#delete shell script if it exists
	os.system('[ -e nos_hydro/xyz/nos2xyz.sh ] && rm nos_hydro/xyz/nos2xyz.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/nos2xyz.sh nos_hydro/xyz/nos2xyz.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e nos_hydro/xyz/neg_m/vert_conv.sh ] && rm nos_hydro/xyz/neg_m/vert_conv.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/vert_conv.sh nos_hydro/xyz/neg_m/vert_conv.sh'.format(code_dir)) 

	#delete shell script if it exists
	os.system('[ -e nos_hydro/xyz/neg_m/gdal_query.py ] && rm nos_hydro/xyz/neg_m/gdal_query.py')
	#copy sh script from DEM_generation code
	os.system('cp {}/gdal_query.py nos_hydro/xyz/neg_m/gdal_query.py'.format(code_dir)) 

	#delete shell script if it exists
	os.system('[ -e nos_hydro/xyz/neg_m/navd88/create_datalist.sh ] && rm nos_hydro/xyz/neg_m/navd88/create_datalist.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/create_datalist.sh nos_hydro/xyz/neg_m/navd88/create_datalist.sh'.format(code_dir)) 

	#NOS BAG
	#delete shell script if it exists
	os.system('[ -e nos_bag/bag2tif2chunks2xyz.sh ] && rm nos_bag/bag2tif2chunks2xyz.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/bag2tif2chunks2xyz.sh nos_bag/bag2tif2chunks2xyz.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e nos_bag/xyz/vert_conv.sh ] && rm nos_bag/xyz/vert_conv.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/vert_conv.sh nos_bag/xyz/vert_conv.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e nos_bag/xyz/gdal_query.py ] && rm nos_bag/xyz/gdal_query.py')
	#copy sh script from DEM_generation code
	os.system('cp {}/gdal_query.py nos_bag/xyz/gdal_query.py'.format(code_dir)) 

	#delete shell script if it exists
	os.system('[ -e nos_bag/xyz/navd88/create_datalist.sh ] && rm nos_bag/xyz/navd88/create_datalist.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/create_datalist.sh nos_bag/xyz/navd88/create_datalist.sh'.format(code_dir))

	print "executing nos_processing script"
	os.system('python nos_processing.py {} {} {} {}'.format(roi_str_gmt, conv_grd_path, bs_dlist, dem_dlist))
else:
	print "Skipping NOS Processing"
# ########################## ENC ################################
if enc_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/bathy/enc')
	print 'Current Directory is', os.getcwd()

	#delete python script if it exists
	os.system('[ -e enc_processing.py ] && rm enc_processing.py')
	#copy python script from DEM_generation code
	os.system('cp {}/enc_processing.py enc_processing.py'.format(code_dir)) 

	print "executing enc_processing script"
	os.system('python enc_processing.py {} {} {} {}'.format(roi_str_gmt, conv_grd_path, bs_dlist))
else:
	print "Skipping ENC Processing"
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
