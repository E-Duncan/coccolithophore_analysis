#!/usr/bin/env python3
"""
Script to regrid dataset using CDO.
Must specify bilinear (BL) or nearest neighbour (NN)
"""

from cdo import *
import sys
import os.path

cdo = Cdo()
cdo.debug = True


ROOT = '/data/datasets/Projects/TuringCoccolithophoreBlooms'
newgrid = ROOT+'/data/AVHRR_reflectance/monthly_mean/Monthly_mean_Rrs_AVHRR_visible_199801.nc'



def regrid(infile,outfile,method):
    if method=='BL':
        cdo.remapbil(newgrid, input=infile, output=outfile)
    elif method=='NN':
        cdo.remapnn(newgrid, input=infile, output=outfile)


def main():
    var = sys.argv[1]
    method = sys.argv[2]
    year = sys.argv[3]
    datapath = sys.argv[4]
    fileformat = sys.argv[5]

    infile = datapath+fileformat.format(var,year)


    print(infile)
    if not os.path.isfile(infile):
        print('File %s does not exist' %infile)
        sys.exit

    outfile = ROOT+'/no_backup/TuringCoccolithophoreBlooms/regridded_data/'+var+'/'+var+'_{}_monthly_mean_regrid_{}.nc'.format(year,method)

    regrid(infile,outfile,method)


main()
