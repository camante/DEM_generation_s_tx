'''
Description:
-Download MB with fetch
-Process by resampling to X cell size


Author:
Chris Amante
Christopher.Amante@colorado.edu

Date:
5/23/2019

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
######################## MB ###########################
print "Current directory is ", os.getcwd()
roi_str_gmt=sys.argv[1]
bs_dlist=sys.argv[2]
#1 arc-sec
#bm_cell=0.00027777777
#1/3 arc-sec res
bm_cell=0.000092592596 

os.system('./download_mb_roi.sh {} {}'.format(roi_str_gmt, bm_cell))
# ####

print "Creating datalist"
os.chdir('xyz')

mb_datalist_cmd='create_datalist.sh mb'
os.system(mb_datalist_cmd)

current_dir=os.getcwd()
add_to_bmaster_cmd='echo ' + current_dir + '/mb.datalist -1 0.01 >> ' + bs_dlist
os.system(add_to_bmaster_cmd)
