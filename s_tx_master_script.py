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
usace_dredge_process='no'
mb_process='no'
nos_process='no'
enc_process='no'
dc_lidar_process='no'
tnm_lidar_process='no'
mx_topo_process='no'
grid_process='no'
bathy_surf_process='yes'
dem_process='yes'
# spatial_meta_process='no'
#################################################################
#################################################################
#################################################################
###################### INITIAL VARIABLES ########################
#################################################################
#################################################################
#################################################################
#Project Area
basename="s_tx"
#Main Directory Paths
main_dir='/media/sf_E_win_lx/COASTAL_Act/camante/'+basename
data_dir=main_dir+'/data'
docs_dir=main_dir+'/docs'
manual_dir=main_dir+'/manual'
software_dir=main_dir+'/software'
code_dir=main_dir+'/code/DEM_generation'+'_'+basename
#Bathy Surface Variables
manual_name_cell_extents_bs=manual_dir+'/data/bathy/bathy_surf/'+basename+'_name_cell_extents_bs.csv'
name_cell_extents_bs=data_dir+'/bathy/bathy_surf/'+basename+'_name_cell_extents_bs.csv'
bs_topo_guide_dlist=data_dir+'/bathy/bathy_surf/topo_guide/topo_guide.datalist'
bs_dlist=data_dir+'/bathy/bathy_surf/'+basename+'_bs.datalist'
bs_ind_dlist=data_dir+'/bathy/bathy_surf/xyz/bathy_surf.datalist'
bs_tifs=data_dir+'/bathy/bathy_surf/tifs'
coast_shp=data_dir+'/coast/'+basename+'_coast'
#use files listed in existing mb1 files at datalist
bs_mb1_var='no'
#DEM Gridding Variables
manual_name_cell_extents_dem=manual_dir+'/software/gridding/'+basename+'_name_cell_extents_dem.csv'
name_cell_extents_dem=software_dir+'/gridding/'+basename+'_name_cell_extents_dem.csv'
dem_dlist=software_dir+'/gridding/'+basename+'_dem.datalist'
dem_smooth_factor=5
#use files listed in existing mb1 files at datalist
dem_mb1_var='no'
#Conversion Grid Variables
ivert='mllw'
overt='navd88'
conv_grd_name='cgrid_'+ivert+'2'+overt+'.tif'
conv_grd_path=data_dir+'/conv_grd/'+conv_grd_name
#Lidar Download Variables
dc_lidar_csv=manual_dir+'/data/dc_lidar/dc_lidar_download_process.csv'
tnm_lidar_man_path=manual_dir+'/data/topo/tnm_lidar/'
tnm_lidar_csv=tnm_lidar_man_path+'tnm_lidar_download_process.csv'

#################################################################
#################################################################
#################################################################
###################### REGION OF INTEREST #######################
#################################################################
#################################################################
#################################################################
west_buff=-98.05
east_buff=-96.45
south_buff=25.70
north_buff=29.05
roi_str_gmt=str(west_buff)+'/'+str(east_buff)+'/'+str(south_buff)+'/'+str(north_buff)
roi_str_ogr=str(west_buff)+' '+str(south_buff)+' '+str(east_buff)+' '+str(north_buff)

#test areas

#E_04 tile test
#E_04_1_9,0.00003086420,-97.25,-97.0,27.75,28.0
#roi_str_gmt='-98.05/-96.45/25.7/29.05'
#roi_str_ogr='-98.05 25.7 -96.45 29.05'

# west_buff=-97.3
# east_buff=-96.95
# south_buff=27.7
# north_buff=28.05
# roi_str_gmt=str(west_buff)+'/'+str(east_buff)+'/'+str(south_buff)+'/'+str(north_buff)
# roi_str_ogr=str(west_buff)+' '+str(south_buff)+' '+str(east_buff)+' '+str(north_buff)

#study area with buffer
study_area_shp=manual_dir+'/data/study_area/'+basename+'_tiles_buff.shp'
#outer ring shp to get surrounding tiles data to ensure seamless across tiles 
study_area_buff_outer_shp=manual_dir+'/data/study_area/'+basename+'_tiles_buff_outer.shp'
#test out with 1 tile (E_04)
#study_area_shp=manual_dir+'/data/study_area/'+basename+'_tiles_test_buff.shp'

#################################################################
#################################################################
#################################################################
###################### DIRECTORY MGMT ###########################
#################################################################
#################################################################
#################################################################
#Creating main directories
main_dir_list=[code_dir,data_dir,docs_dir,manual_dir,software_dir]
for i in main_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#Creating main data subdirectories
data_dir_list=[data_dir+'/bathy',data_dir+'/coast',data_dir+'/conv_grd',data_dir+'/dc_lidar',data_dir+'/topo/tnm_lidar',data_dir+'/grids']
for i in data_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#Creating main bathy data subdirectories
bathy_dir_list=[data_dir+'/bathy/usace_dredge', data_dir+'/bathy/mb', data_dir+'/bathy/nos', data_dir+'/bathy/enc', data_dir+'/bathy/bathy_surf']
for i in bathy_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#Creating main docs subdirectories
docs_dir_list=[docs_dir+'/resources',docs_dir+'/report']
for i in docs_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#Creating main manual subdirectories
manual_dir_list=[manual_dir+'/data/coast',manual_dir+'/data/study_area', manual_dir+'/data/grids/ncei']
for i in manual_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

# #Creating main DEM grids subdirectories available on Digital Coast / National Map
# grid_dir_list=[data_dir+'/grids/ncei',data_dir+'/grids/usgs']
# for i in grid_dir_list:
# 	if not os.path.exists(i):
# 		print 'creating subdir', i
# 		os.makedirs(i)

#Creating main software subdirectories
software_dir_list=[software_dir+'/gridding']
for i in software_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#################################################################
#################################################################
#################################################################
###################### MASTER DATALISTS #########################
#################################################################
#################################################################
#################################################################
#Create Empty Bathy Surface and DEM Master datalists if they don't exist
#Add topo guide to bathy surface datalist
create_bs_dlist='''if [ ! -e {} ] ; 
then touch {}
echo {} -1 0.000001 >> {}
fi'''.format(bs_dlist,bs_dlist,bs_topo_guide_dlist,bs_dlist)
os.system(create_bs_dlist)

create_dem_dlist='''if [ ! -e {} ] ; 
then touch {}
echo {} -1 0.000001 >> {}
fi'''.format(dem_dlist,dem_dlist,bs_ind_dlist,dem_dlist)
os.system(create_dem_dlist)

#################################################################
#################################################################
#################################################################
###################### NAME CELL EXTENTS ########################
#################################################################
#################################################################
#################################################################
#Copy Name Cell Extents from Manual Directories

#delete csv if it exists
os.system('[ -e {} ] && rm {}'.format(name_cell_extents_bs,name_cell_extents_bs))
# copy csv from manual dir
os.system('cp {} {}'.format(manual_name_cell_extents_bs,name_cell_extents_bs)) 

#delete csv if it exists
os.system('[ -e {} ] && rm {}'.format(name_cell_extents_dem,name_cell_extents_dem))
# copy csv from manual dir
os.system('cp {} {}'.format(manual_name_cell_extents_dem,name_cell_extents_dem)) 

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
	conv_grd_cmd='waffles --verbose -R {} -E 1s -O {} vdatum:ivert=mllw:overt=navd88:region=3'.format(roi_str_gmt,conv_grd_name)
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
#manually created shp in Global Mapper / ArcGIS (s_tx_tiles.shp) 
#created name_cell_extents with arcpy get_poly_coords.py (name_cell_extents_bs.csv; name_cell_extents_DEM.csv) 
#manually created study area buffer in ArcMap (s_tx_tiles_buff.shp)
#manually created outer buffer to grab adjacenet NCEI tiles DEMs (s_tx_tiles_buff_outer.shp) using arcmap erase(s_tx_tiles_buff.shp,s_tx_tiles.shp)
# #################################################################
# ######################## COASTLINE ##############################
# #################################################################
if coast_process=='yes':
	os.chdir(data_dir+'/coast')
	print 'Current Directory is', os.getcwd()

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
	os.system('./coast_processing.py {} {} {} {} {} {} {}'.format(basename,main_dir,west_buff,east_buff,south_buff,north_buff,study_area_shp))
else:
	print "Skipping Coastline Processing"

# #################################################################
# ########################## BATHY ################################
# #################################################################
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
	os.system('./usace_dredge_processing.py {} {} {} {}'.format(roi_str_gmt, conv_grd_path, bs_dlist, dem_dlist))
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
	os.system('./mb_processing.py {} {}'.format(roi_str_gmt, bs_dlist))
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
	os.system('./nos_processing.py {} {} {} {}'.format(roi_str_gmt, conv_grd_path, bs_dlist, dem_dlist))
else:
	print "Skipping NOS Processing"
# ########################## ENC ################################
if enc_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/bathy/enc')
	print 'Current Directory is', os.getcwd()

	######### CODE MANAGEMENT #########
	os.system('mkdir -p xyz')
	os.system('mkdir -p xyz/neg')
	os.system('mkdir -p xyz/neg/navd88')

	#delete python script if it exists
	os.system('[ -e enc_processing.py ] && rm enc_processing.py')
	#copy python script from DEM_generation code
	os.system('cp {}/enc_processing.py enc_processing.py'.format(code_dir)) 

	#delete shell script if it exists
	os.system('[ -e xyz/pos2neg.sh ] && rm xyz/pos2neg.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/pos2neg.sh xyz/pos2neg.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e xyz/neg/vert_conv.sh ] && rm xyz/neg/vert_conv.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/vert_conv.sh xyz/neg/vert_conv.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e xyz/neg/gdal_query.py ] && rm xyz/neg/gdal_query.py')
	#copy sh script from DEM_generation code
	os.system('cp {}/gdal_query.py xyz/neg/gdal_query.py'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e xyz/neg/navd88/create_datalist.sh ] && rm xyz/neg/navd88/create_datalist.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/create_datalist.sh xyz/neg/navd88/create_datalist.sh'.format(code_dir))

	print "executing enc_processing script"
	os.system('./enc_processing.py {} {} {}'.format(roi_str_gmt, conv_grd_path, bs_dlist))
else:
	print "Skipping ENC Processing"
#############################################################
################## DIGITAL COAST LIDAR ######################
#############################################################
if dc_lidar_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/dc_lidar')
	print 'Current Directory is', os.getcwd()
	
	######### CODE MANAGEMENT #########

	#delete shell script if it exists
	os.system('[ -e download_process_lidar.sh ] && rm download_process_lidar.sh')
	#copy shell script from DEM_generation code
	os.system('cp {}/download_process_lidar.sh download_process_lidar.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e laz2xyz.sh ] && rm laz2xyz.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/laz2xyz.sh laz2xyz.sh'.format(code_dir)) 

	os.system('[ -e separate_pos_neg.sh ] && rm separate_pos_neg.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/separate_pos_neg.sh separate_pos_neg.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e create_datalist.sh ] && rm create_datalist.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/create_datalist.sh create_datalist.sh'.format(code_dir)) 

	print "executing dc_lidar_processing script"
	os.system('./download_process_lidar.sh {} {} {} {}'.format(dc_lidar_csv,study_area_shp,bs_dlist,dem_dlist))
	####
else:
	print "Skipping DC Lidar Processing"

#############################################################
################## TNM LIDAR ################################
#############################################################
if tnm_lidar_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/topo/tnm_lidar')
	print 'Current Directory is', os.getcwd()
	
	######### CODE MANAGEMENT #########

	#delete shell script if it exists
	os.system('[ -e tnm_download_process_lidar.sh ] && rm tnm_download_process_lidar.sh')
	#copy shell script from DEM_generation code
	os.system('cp {}/tnm_download_process_lidar.sh tnm_download_process_lidar.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e laz2xyz_repro_latlon_m.sh ] && laz2xyz_repro_latlon_m.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/laz2xyz_repro_latlon_m.sh laz2xyz_repro_latlon_m.sh'.format(code_dir)) 

	os.system('[ -e separate_pos_neg.sh ] && rm separate_pos_neg.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/separate_pos_neg.sh separate_pos_neg.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e create_datalist.sh ] && rm create_datalist.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/create_datalist.sh create_datalist.sh'.format(code_dir)) 

	print "executing tnm_lidar_processing script"
	os.system('./tnm_download_process_lidar.sh {} {} {} {}'.format(tnm_lidar_man_path,tnm_lidar_csv,bs_dlist,dem_dlist))
	####
else:
	print "Skipping TNM Lidar Processing"

#############################################################
################## MX TOPO ##################################
#############################################################
if mx_topo_process=='yes':
	os.system('cd')
	os.chdir(manual_dir+'/data/topo/mx')
	print 'Current Directory is', os.getcwd()
	
	######### CODE MANAGEMENT #########
	os.system('mkdir -p xyz')

	#delete shell script if it exists
	os.system('[ -e mx_topo_processing.sh ] && rm mx_topo_processing.sh')
	#copy shell script from DEM_generation code
	os.system('cp {}/mx_topo_processing.sh mx_topo_processing.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e xyz/create_datalist.sh ] && rm xyz/create_datalist.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/create_datalist.sh xyz/create_datalist.sh'.format(code_dir)) 

	print "executing mc_topo_processing script"
	os.system('./mx_topo_processing.sh {}'.format(dem_dlist))
	####
else:
	print "Skipping MX Topo Processing"

#############################################################
################## EXISTING GRIDS ###########################
#############################################################
if grid_process=='yes':
	os.system('cd')
	os.chdir(manual_dir+'/data/grids/ncei')
	print 'Current Directory is', os.getcwd()
	
	######### CODE MANAGEMENT #########
	os.system('mkdir -p xyz')

	#delete shell script if it exists
	os.system('[ -e grids_ncei_processing.sh.sh ] && rm grids_ncei_processing.sh')
	#copy shell script from DEM_generation code
	os.system('cp {}/grids_ncei_processing.sh grids_ncei_processing.sh'.format(code_dir))

	#delete shell script if it exists
	os.system('[ -e xyz/create_datalist.sh ] && rm xyz/create_datalist.sh')
	#copy sh script from DEM_generation code
	os.system('cp {}/create_datalist.sh xyz/create_datalist.sh'.format(code_dir)) 

	print "executing grids_ncei_processing.sh script"
	os.system('./grids_ncei_processing.sh {} {} {}'.format(study_area_buff_outer_shp,bs_dlist,dem_dlist))
	####
else:
	print "Skipping Grids_ncei Processing"
# # #################################################################
# # #################################################################
# # #################################################################
# # ####################### BATHY SURFACE ###########################
# # #################################################################
# # #################################################################
# # #################################################################
if bathy_surf_process=='yes':
	os.system('cd')
	os.chdir(data_dir+'/bathy/bathy_surf')
	print 'Current Directory is', os.getcwd()
	
	######### CODE MANAGEMENT #########

	#delete shell script if it exists
	os.system('[ -e create_bs.sh ] && rm create_bs.sh')
	#copy shell script from DEM_generation code
	os.system('cp {}/create_bs.sh create_bs.sh'.format(code_dir))

	print "executing create_bs.sh script"
	os.system('./create_bs.sh {} {} {} {}'.format(name_cell_extents_bs,bs_dlist,coast_shp,bs_mb1_var))
	####
else:
	print "Skipping Bathy Surface Processing"

# # # #################################################################
# # # #################################################################
# # # #################################################################
# # # ####################### DEM GENERATION ##########################
# # # #################################################################
# # # #################################################################
# # # #################################################################
if dem_process=='yes':
	os.system('cd')
	os.chdir(software_dir+'/gridding')
	print 'Current Directory is', os.getcwd()
	
	######### CODE MANAGEMENT #########

	#delete shell script if it exists
	os.system('[ -e create_dem.sh ] && rm create_dem.sh')
	#copy shell script from DEM_generation code
	os.system('cp {}/create_dem.sh create_dem.sh'.format(code_dir))

	#delete py script if it exists
	os.system('[ -e smooth_dem_bathy.py ] && rm smooth_dem_bathy.py')
	#copy py script from DEM_generation code
	os.system('cp {}/smooth_dem_bathy.py smooth_dem_bathy.py'.format(code_dir))

	print "executing create_dem.sh script"
	os.system('./create_dem.sh {} {} {} {}'.format(name_cell_extents_dem,dem_dlist,dem_smooth_factor,dem_mb1_var))
	####
else:
	print "Skipping DEM Processing"
