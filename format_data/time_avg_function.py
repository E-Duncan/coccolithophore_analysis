from cdo import *
from multiprocessing import Pool
import sys
import os.path

cdo = Cdo()
cdo.debug = True


ROOT = '/data/datasets/Projects/TuringCoccolithophoreBlooms'


def main():
    var = sys.argv[1]
    year = sys.argv[2]
    month = sys.argv[3]


    infile = ROOT+'/no_backup/TuringCoccolithophoreBlooms/raw_data/'+var+'/'+var+'_{}_{}.nc'.format(year,month)
    print(infile)
    if not os.path.isfile(infile):
        print('File %s does not exist' %infile)
        sys.exit

    outfile = ROOT+'/no_backup/TuringCoccolithophoreBlooms/temporal_avg/'+var+'/'+var+'_{}_{}_monthly_mean.nc'.format(year,month)

    cdo.timmean(input=infile,output=outfile)


main()
~       
