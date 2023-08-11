from make_dataframe_function import make_prov_file
import numpy as np


provinces = np.arange(0,53)

#Load in longhurst shape file
import fiona
mask_path = '/data/datasets/Projects/TuringCoccolithophoreBlooms/province_files/Longhurst_world_v4_2010.shp'
shapefile = fiona.open(mask_path)
with fiona.open(mask_path) as shapefile:
    shapes = [feature for feature in shapefile]


#Loop over provinces
for p in provinces:
    geometries = [shapes[p]['geometry']]
    make_prov_file(p,geometries)
