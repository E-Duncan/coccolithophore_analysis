#!/usr/bin/env python3
"""
Script to regrid dataset using CDO.
Must specify bilinear (BL) or nearest neighbour (NN)
"""

from cdo import *
from multiprocessing import Pool
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
    month = sys.argv[4]
    temporal = sys.argv[5]

    infile = ROOT+'/no_backup/TuringCoccolithophoreBlooms/temporal_avg/'+var+'/'+var+'_{}_{}_monthly_{}.nc'.format(year,month,temporal)
    print(infile)
    if not os.path.isfile(infile):
        print('File %s does not exist' %infile)
        sys.exit

    outfile = ROOT+'/no_backup/TuringCoccolithophoreBlooms/regridded_data/'+var+'/'+var+'_{}_{}_monthly_{}_regrid_{}.nc'.format(year,month,temporal,method)
    regrid(infile,outfile,method)

main()
