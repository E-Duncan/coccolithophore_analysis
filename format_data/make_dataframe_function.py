import numpy as np
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import pandas as pd
from datetime import datetime
import glob
import sys

def load_data(filepath,preprocess=None):
    ds=xr.open_mfdataset(filepath,mask_and_scale=True,preprocess=preprocess)
    return ds

def add_time_dim(xda):
    xda = xda.expand_dims(time = [datetime.now()])
    return xda

ROOT = "/data/datasets/Projects/TuringCoccolithophoreBlooms"

data_filepath = ROOT+"/no_backup/TuringCoccolithophoreBlooms/regridded_data/"
varnames = ["analysed_sst","wind_speed","wind_speed","wind_stress","wind_stress","sla","mlotst","par"]
path_end = ["analysed_sst/","CMEMS_wind_speed/*mean","CMEMS_wind_speed/*std","CMEMS_wind_stress/*mean","CMEMS_wind_stress/*std","sla/","mlotst/","par/"]
df_names = ["SST","Wind speed mean","Wind speed std","Wind stress mean","Wind stress std","SLA","MLD","PAR"]
filt = [False, True, True, True, True, False, False, False]

def make_prov_file(province_no,geometries):

    ##LOAD reflectance file
    filtered_filepath = ROOT+"/data/rrs_masked_by_sea_ice.nc"
    varname = "filtered_remote_sensing_reflectance"
    ds = xr.open_dataset(filtered_filepath)
    print(ds)
    rrs = ds[varname]
    rrs.rio.set_crs(4326, inplace=True)
    rrs = rrs.rio.clip(geometries)

    dts = pd.to_datetime(rrs.time.values) + pd.offsets.MonthBegin(-1)
    print(dts[0].date(),rrs.time.values[0])
    dts = [i.date() for i in dts]
    rrs = rrs.assign_coords(time=("time", dts))


    for i,v in enumerate(varnames):
        print(v)
        ds = load_data(data_filepath+path_end[i]+"*.nc")
        var = ds[v]

        if filt[i]==True:
            var.loc[:, 80:90,:] = np.nan
            var.loc[:, -90:-80,:] = np.nan
        var.rio.write_nodata(np.nan, inplace=True) #can't install rioxarray at the moment
        var.rio.set_crs(4326, inplace=True)
        var = var.rio.clip(geometries)
        var = var.rename(df_names[i])
        if pd.to_datetime(var.time.values)[0].date!=1:
            dts = pd.to_datetime(var.time.values)+pd.offsets.MonthBegin(-1)
            dts = [i.date() for i in dts]
            print(dts[0],var.time.values[0])
            var = var.assign_coords(time=("time", dts))
        print(var)
        rrs = xr.merge([rrs, var],join='inner')
        print(rrs)

    rrs = rrs.assign_coords(time=("time", pd.to_datetime(rrs.time.values)))
    rrs = rrs.rename({'filtered_remote_sensing_reflectance':'rrs'})
    rrs.to_netcdf(ROOT+'/no_backup/TuringCoccolithophoreBlooms/province_dataframes/province_'+str(province_no)+'.nc')

def make_prov_file(province_no,geometries):

    ##LOAD reflectance file
    filtered_filepath = ROOT+"/data/rrs_masked_by_sea_ice.nc"
    varname = "filtered_remote_sensing_reflectance"
    ds = xr.open_dataset(filtered_filepath)
    print(ds)
    rrs = ds[varname]
    rrs.rio.set_crs(4326, inplace=True)
    rrs = rrs.rio.clip(geometries)

    dts = pd.to_datetime(rrs.time.values) + pd.offsets.MonthBegin(-1)
    print(dts[0].date(),rrs.time.values[0])
    dts = [i.date() for i in dts]
    rrs = rrs.assign_coords(time=("time", dts))


    for i,v in enumerate(varnames):
        print(v)
        ds = load_data(data_filepath+path_end[i]+"*.nc")
        var = ds[v]

        if filt[i]==True:
            var.loc[:, 80:90,:] = np.nan
            var.loc[:, -90:-80,:] = np.nan
        var.rio.write_nodata(np.nan, inplace=True) #can't install rioxarray at the moment
        var.rio.set_crs(4326, inplace=True)
        var = var.rio.clip(geometries)
        var = var.rename(df_names[i])
        if pd.to_datetime(var.time.values)[0].date!=1:
            dts = pd.to_datetime(var.time.values)+pd.offsets.MonthBegin(-1)
            dts = [i.date() for i in dts]
            print(dts[0],var.time.values[0])
            var = var.assign_coords(time=("time", dts))
        print(var)
        rrs = xr.merge([rrs, var],join='inner')
        print(rrs)

    rrs = rrs.assign_coords(time=("time", pd.to_datetime(rrs.time.values)))
    rrs = rrs.rename({'filtered_remote_sensing_reflectance':'rrs'})
    rrs.to_netcdf(ROOT+'/no_backup/TuringCoccolithophoreBlooms/province_dataframes/province_'+str(province_no)+'.nc')
