

# ==== binning ============================================

def regular_bins(df):
    output = pd.DataFrame()
    for profile_id, profile in df.groupby('profile_id'):
        levels = np.arange(np.ceil(profile.depth.min()/10),
                           np.round(profile.depth.max()/10),
                           dtype='i') * 10
        levels = levels[levels>=10]
        tmp = []
        for z in levels:
            subset = profile[(profile.depth >= (z-5)) & (profile.depth <= (z+5))]
            tmp.append(subset.mean())
            tmp[-1]['depth'] = z
        tmp = pd.DataFrame(tmp)
        tmp['profile_id'] = profile_id
        output = output.append(tmp)

    output['depth'] = output['depth'].astype('i')
    output = output.set_index(['depth', 'profile_id'])
    return output


def binDataset(ds, varname='fl'):
    levels = np.arange(np.floor(ds.depth.min()/10),
                       np.round(ds.depth.max()/10),
                       dtype='i') * 10
    binned = []
    for z in levels:
        tmp = ds.where((ds.depth>z-5) & (ds.depth<=z+5), np.nan)
        tmp = tmp.dropna(dim='obs', how='all')
        tmp = tmp.dropna(dim='profile', how='all')
        if tmp[varname].any():
            tmp = tmp.mean(dim='obs')
            tmp = tmp.expand_dims('depth_bins').assign_coords(depth_bins=[z])
            binned.append(tmp)

    binned = xr.merge(binned)
    return binned


def binDataArray(ds):
    levels = np.arange(np.floor(ds.depth.min()/10),
                       np.round(ds.depth.max()/10),
                       dtype='i') * 10
    binned = []
    for z in levels:
        tmp = ds.where((ds.depth>z-5) & (ds.depth<=z+5), np.nan)
        tmp = tmp.dropna(dim='profile', how='all')
        tmp = tmp.mean(dim='obs')
        tmp = tmp.expand_dims('depth_bins').assign_coords(depth_bins=[z])
        binned.append(tmp)

    binned = xr.merge(binned)
    return binned




# ========================================================

import xarray as xr

ds = xr.open_dataset('0014.nc')
ds['density'] = ds.sigma + 1e3

df = ds.sel(dive=10).reset_coords().to_dataframe().reset_index()
df = df[['depth', 'temp', 'sal', 'density']]
df['time'] = pd.date_range('2018-1-1T00:00:00', periods=df.shape[0], freq='8S')
df = df.set_index('time')
profile = df.to_xarray()


tmp = ds.sel(dive=10).reset_coords()[['datetime', 'lat', 'lon', 'datetime_uv', 'latitude_uv', 'longitude_uv', 'latitude_uv', 'longitude_uv', 'u_depth_mean', 'v_depth_mean']]
profile = xr.merge([profile, tmp])
profile = profile.rename({'lat': 'profile_lat', 'lon': 'profile_lon', 'datetime_uv': 'time_uv', 'u_depth_mean': 'u', 'v_depth_mean': 'v', 'latitude_uv': 'lat_uv', 'longitude_uv': 'lon_uv'})
data_model = np.nan * np.ones(profile.time.shape)
qc_model = np.ones(profile.time.shape)

profile['profile_id'] = 10
profile['profile_time_qc'] = 9
profile['time_qc'] = xr.DataArray(9*qc_model, dims=['time'])
profile['profile_lat_qc'] = 9
profile['profile_lon_qc'] = 9
profile['pressure'] = xr.DataArray(data_model, dims=['time'])
profile['pressure_qc'] = xr.DataArray(0 * qc_model, dims=['time'])
profile['lat'] = xr.DataArray(data_model, dims=['time'])
profile['lat_qc'] = xr.DataArray(9*qc_model, dims=['time'])
profile['lon'] = xr.DataArray(data_model, dims=['time'])
profile['lon_qc'] = xr.DataArray(9*qc_model, dims=['time'])
profile['depth_qc'] = xr.DataArray(0*qc_model, dims=['time'])
profile['temp_qc'] = xr.DataArray(0*qc_model, dims=['time'])
profile['sal_qc'] = xr.DataArray(0*qc_model, dims=['time'])
profile['density_qc'] = xr.DataArray(0*qc_model, dims=['time'])
profile['cndc'] = xr.DataArray(data_model, dims=['time'])
profile['cndc_qc'] = xr.DataArray(9*qc_model, dims=['time'])
#profile['time_uv'] = xr.DataArray(data_model, dims=['time'])
profile['time_uv_qc'] = 9
profile['lat_uv_qc'] = 9
profile['lon_uv_qc'] = 9
profile['u_qc'] = 9
profile['v_qc'] = 9

profile['platform'] = np.nan
profile['instrument_ctd'] = np.nan



# profile = profile.rename({'datetime': 'time', 'datetime_uv': 'time_uv', 'temp': 'temperature', 'sal': 'salinity', 'fl': 'fluorescence'})
# profile = profile[['depth', 'temp', 'sal', 'density', 'datetime', 'lat', 'lon', 'datetime_uv', 'latitude_uv', 'longitude_uv']]

cfgname = 'spray_ngdac'
NGDAC30(profile, 'ngdac_test.nc', cfgname='spray_ngdac')

# ====

filename1 = '/Users/castelao/work/Spray/xglider/others/examples/ngdac/sp022-20170209T175600_rt.nc'
filename2 = '/Users/castelao/work/Spray/xglider/ngdac_test.nc'

nc1 = netCDF4.Dataset(filename1)
nc2 = netCDF4.Dataset(filename2)

for v in [v for v in nc1.variables.keys() if v not in nc2.variables.keys()]:
    print("Missing variable: {}".format(v))

for v in [v for v in nc1.variables.keys() if v in nc2.variables.keys()]:
    if nc1[v].dtype != nc2[v].dtype:
        print("Dtype mismatch [{}]: {} x {}".format(v, nc1[v].dtype, nc2[v].dtype))

for v in [v for v in nc1.variables.keys() if v in nc2.variables.keys()]:
    if nc1[v].dimensions != nc2[v].dimensions:
        print("Dimensions mismatch [{}]: {} x {}".format(v, nc1[v].dimensions, nc2[v].dimensions))

for v in [v for v in nc1.variables.keys() if v in nc2.variables.keys()]:
    for a in nc1[v].ncattrs():
        if a not in nc2[v].ncattrs():
            print("Missing attribute {}:{} = {}".format(v, a, nc1[v].getncattr(a)))

for v in [v for v in nc1.variables.keys() if v in nc2.variables.keys()]:
    for a in nc1[v].ncattrs():
        try:
            if nc1[v].getncattr(a) != nc2[v].getncattr(a):
                print("Attribute mismatch {}:{} -> {} versus {}".format(v, a, nc1[v].getncattr(a), nc2[v].getncattr(a)))
        except:
            pass


nc1.close()
nc2.close()


import pandas as pd
from shapely.geometry import MultiPoint


def convert_datetime(ds, drop=True, inplace=False):
    """Convert datetime variable
    """
    if not inplace:
        ds = ds.copy(deep=True)

    ds['time'] = (ds['datetime'] - np.datetime64('1970-01-01T00:00:00')
        ) / np.timedelta64(1, 's')
    for a in ds.datetime.attrs:
        ds.time.attrs[a] = ds.datetime.attrs[a]

    ds.time.attrs['standard_name'] = 'time'
    ds.time.attrs['long_name'] = "time"
    ds.time.attrs['units'] = "seconds since 1970-01-01 00:00:00"
    ds.time.attrs['axis'] = "T"
    ds.time.attrs['calendar'] = "gregorian"
    if 'datetime' in ds.coords:
        ds.set_coords('time', inplace=True)
    if drop:
        del(ds['datetime'])

    if not inplace:
        return ds


# Assign attributes
for a in cfg['global_attributes']:
    ds.attrs[a] = cfg['global_attributes'][a]

for v in cfg['variables']:
    if (v in ds.variables) and ('attrs' in cfg['variables'][v]):
        for a in cfg['variables'][v]['attrs']:
            ds[v].attrs[a] = cfg['variables'][v]['attrs'][a]


for a in [a for a in ds.attrs if ds.attrs[a] == None]:
    del(ds.attrs[a])
    



import matplotlib.pyplot as plt
from SprayTools.matlab import SprayMatfile

filename='/Users/castelao/work/Spray/data/mat/15C02001.mat'
filename='/Users/castelao/work/Spray/data/mat/16305001.mat'
filename='/Users/castelao/work/Spray/data/mat/17504901.mat'
filename='/Users/castelao/work/Spray/data/mat/16705301.mat'
ds = SprayMatfile(filename)
ds = ds.bindata
plt.contourf(ds.profile, ds.depth, np.log10(ds.isel(mission=0).fl), 25)
plt.colorbar()
plt.show()



def _contourf(ax, da, scale):
    da = da.dropna(dim='depth', how='all')
    da = da.where((da>0) | (da.isnull()), np.exp(scale.min()))

    cs = ax.contourf(da.profile, da.depth, np.log(da),
            scale, extend='both')

    ax.set_ylabel('Depth [m]')
    ax.invert_yaxis()
    return cs



fig = plt.figure(figsize=(6, 6))

axes = [
        plt.axes([0.07, 0.530, 0.92, 0.425]),
        plt.axes([0.07, 0.100, 0.92, 0.425]),
        plt.axes([0.45, 0.028, 0.5, 0.036])
        ]

scale = np.arange(-3, 1.1, 0.10)
cs = []
cs.append(_contourf(axes[0], ds.fl.isel(depth=ds.depth<=120), scale))
axes[0].xaxis.set_visible(False)
cs.append(_contourf(axes[1], ds.fl.isel(depth=ds.depth>=120), scale))
# plt.subplots_adjust(bottom=0.15, top=0.95)
# cax = plt.axes([0.4, 0.075, 0.5, 0.020])
cax = axes[2]
clevels = [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]
cbar = fig.colorbar(cs[0], cax=cax, orientation='horizontal',
                    ticks=np.log(clevels))
cbar.ax.set_xticklabels([str(c) for c in clevels])

fig.suptitle(name)

plt.show()



fig, axs = plt.subplots(2, 1)
scale = np.arange(-3, 1.1, 0.10)
cs = []
cs.append(_contourf(axs[0], ds.fl.isel(depth=ds.depth<=120), scale))
axs[0].xaxis.set_visible(False)
cs.append(_contourf(axs[1], ds.fl.isel(depth=ds.depth>=120), scale))
# plt.subplots_adjust(bottom=0.15, top=0.95)
# cax = plt.axes([0.4, 0.075, 0.5, 0.020])
cax = axs[0]
clevels = [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]
# cbar = fig.colorbar(cs[0], cax=cax, orientation='horizontal',
#                     ticks=np.log(clevels))
# cbar.ax.set_xticklabels([str(c) for c in clevels])
fig.colorbar(cs[0], ax=axs, orientation='horizontal', fraction=.05)

fig.suptitle(name)

plt.show()



import numpy as np
import pandas as pd
import xarray as xr

from SprayTools.matlab import SprayMatfile
filename = '/Users/castelao/work/Spray/SprayDB/18102201.mat'
ds = SprayMatfile(filename)
ds = ds['bindata']
# ds = ds.isel(profile=ds.profile<=3)
# ds = ds.isel(depth=range(5))
ds.attrs = {}



#ds = xr.open_dataset('/Users/castelao/xglider/0014.nc')
#ds = ds.isel(dive=ds.dive<10)
#ds = ds.rename({'dive': 'profile'})
#ds.drop
#ds['density'] = ds.sigma + 1e3
#
#df = ds.sel(dive=10).reset_coords().to_dataframe().reset_index()
#df = df[['depth', 'temp', 'sal', 'density']]
#df['time'] = pd.date_range('2018-1-1T00:00:00', periods=df.shape[0], freq='8S')
#df = df.set_index('time')
#mission = df.to_xarray()
#
#
#tmp = ds.sel(dive=10).reset_coords()[['datetime', 'lat', 'lon', 'datetime_uv', 'latitude_uv', 'longitude_uv', 'latitude_uv', 'longitude_uv', 'u_depth_mean', 'v_depth_mean']]
#profile = xr.merge([profile, tmp])
#profile = profile.rename({'lat': 'profile_lat', 'lon': 'profile_lon', 'datetime_uv': 'time_uv', 'u_depth_mean': 'u', 'v_depth_mean': 'v', 'latitude_uv': 'lat_uv', 'longitude_uv': 'lon_uv'})
#data_model = np.nan * np.ones(profile.time.shape)
#qc_model = np.ones(profile.time.shape)
#
#profile['profile_id'] = 10
#profile['profile_time_qc'] = 9
#profile['time_qc'] = xr.DataArray(9*qc_model, dims=['time'])
#profile['profile_lat_qc'] = 9
#profile['profile_lon_qc'] = 9
#profile['pressure'] = xr.DataArray(data_model, dims=['time'])
#profile['pressure_qc'] = xr.DataArray(0 * qc_model, dims=['time'])
#profile['lat'] = xr.DataArray(data_model, dims=['time'])
#profile['lat_qc'] = xr.DataArray(9*qc_model, dims=['time'])
#profile['lon'] = xr.DataArray(data_model, dims=['time'])
#profile['lon_qc'] = xr.DataArray(9*qc_model, dims=['time'])
#profile['depth_qc'] = xr.DataArray(0*qc_model, dims=['time'])
#profile['temp_qc'] = xr.DataArray(0*qc_model, dims=['time'])
#profile['sal_qc'] = xr.DataArray(0*qc_model, dims=['time'])
#profile['density_qc'] = xr.DataArray(0*qc_model, dims=['time'])
#profile['cndc'] = xr.DataArray(data_model, dims=['time'])
#profile['cndc_qc'] = xr.DataArray(9*qc_model, dims=['time'])
##profile['time_uv'] = xr.DataArray(data_model, dims=['time'])
#profile['time_uv_qc'] = 9
#profile['lat_uv_qc'] = 9
#profile['lon_uv_qc'] = 9
#profile['u_qc'] = 9
#profile['v_qc'] = 9
#
#profile['platform'] = np.nan
#profile['instrument_ctd'] = np.nan

# ds = ds.reset_coords().assign_coords(mission=['sp064-20180619T1733'])
ds = ds.isel(mission=0)
ds['trajectoryIndex'] = xr.DataArray(np.zeros(ds.profile.shape, dtype='i'), dims='profile')

#ds['rowSize']


# profile = profile[['depth', 'temp', 'sal', 'density', 'datetime', 'lat', 'lon', 'datetime_uv', 'latitude_uv', 'longitude_uv']]

# import pdb; pdb.set_trace()
ds = ds.reset_coords()
# ds = ds[['mission', 'profile', 'time', 'lat', 'lon', 'trajectoryIndex', 'temp', 'sal']]
ds = ds[['profile', 'time', 'lat', 'lon', 'trajectoryIndex', 'temp', 'sal']]

dim = 'depth'
varnames = [v for v in ds.variables if (dim in ds[v].dims)]
# tmp = ds.reset_coords()[varnames].to_dataframe().dropna(how='all').sort_values(['profile', 'depth']).reset_index().reset_index().rename(index=str, columns={'index': 'obs'}).set_index('obs')
# import pdb; pdb.set_trace()
# tmp = ds[varnames].to_dataframe().dropna(how='all').sort_values(['profile', 'depth']).reset_index().reset_index().rename(index=str, columns={'index': 'obs'}).set_index(['mission', 'obs'])
tmp = ds[varnames].to_dataframe().dropna(how='all').sort_values(['profile', 'depth']).reset_index().reset_index().rename(index=str, columns={'index': 'obs'}).set_index(['obs'])
ds['row_size'] = tmp.groupby('profile').count()['depth'].to_xarray()
tmp = tmp.to_xarray().drop('profile')
for v in tmp:
    # for a in ds[v].attrs:
    #     tmp[v].attrs[a] = ds[v].attrs[a]
    ds[v] = tmp[v]

import pdb; pdb.set_trace()
#ds = ds.expand_dims('mission').assign_coords(mission=['sp064-20180619T1733'])
ds = ds.assign_coords(mission=['sp064-20180619T1733'])


cfgname = 'spray_ngdac'
from netcdf import NGDAC30
NGDAC30(ds, 'ngdac_test.nc', cfgname='spray_ngdac')
import sys; sys.exit()

# ====

filename1 = '/Users/castelao/work/Spray/xglider/others/examples/ngdac/sp022-20170209T175600_rt.nc'
filename2 = '/Users/castelao/work/Spray/xglider/ngdac_test.nc'

nc1 = netCDF4.Dataset(filename1)
nc2 = netCDF4.Dataset(filename2)

for v in [v for v in nc1.variables.keys() if v not in nc2.variables.keys()]:
    print("Missing variable: {}".format(v))

for v in [v for v in nc1.variables.keys() if v in nc2.variables.keys()]:
    if nc1[v].dtype != nc2[v].dtype:
        print("Dtype mismatch [{}]: {} x {}".format(v, nc1[v].dtype, nc2[v].dtype))

for v in [v for v in nc1.variables.keys() if v in nc2.variables.keys()]:
    if nc1[v].dimensions != nc2[v].dimensions:
        print("Dimensions mismatch [{}]: {} x {}".format(v, nc1[v].dimensions, nc2[v].dimensions))

for v in [v for v in nc1.variables.keys() if v in nc2.variables.keys()]:
    for a in nc1[v].ncattrs():
        if a not in nc2[v].ncattrs():
            print("Missing attribute {}:{} = {}".format(v, a, nc1[v].getncattr(a)))

for v in [v for v in nc1.variables.keys() if v in nc2.variables.keys()]:
    for a in nc1[v].ncattrs():
        try:
            if nc1[v].getncattr(a) != nc2[v].getncattr(a):
                print("Attribute mismatch {}:{} -> {} versus {}".format(v, a, nc1[v].getncattr(a), nc2[v].getncattr(a)))
        except:
            pass


nc1.close()
nc2.close()


import pandas as pd
from shapely.geometry import MultiPoint


def convert_datetime(ds, drop=True, inplace=False):
    """Convert datetime variable
    """
    if not inplace:
        ds = ds.copy(deep=True)

    ds['time'] = (ds['datetime'] - np.datetime64('1970-01-01T00:00:00')
        ) / np.timedelta64(1, 's')
    for a in ds.datetime.attrs:
        ds.time.attrs[a] = ds.datetime.attrs[a]

    ds.time.attrs['standard_name'] = 'time'
    ds.time.attrs['long_name'] = "time"
    ds.time.attrs['units'] = "seconds since 1970-01-01 00:00:00"
    ds.time.attrs['axis'] = "T"
    ds.time.attrs['calendar'] = "gregorian"
    if 'datetime' in ds.coords:
        ds.set_coords('time', inplace=True)
    if drop:
        del(ds['datetime'])

    if not inplace:
        return ds


# Assign attributes
for a in cfg['global_attributes']:
    ds.attrs[a] = cfg['global_attributes'][a]

for v in cfg['variables']:
    if (v in ds.variables) and ('attrs' in cfg['variables'][v]):
        for a in cfg['variables'][v]['attrs']:
            ds[v].attrs[a] = cfg['variables'][v]['attrs'][a]


for a in [a for a in ds.attrs if ds.attrs[a] == None]:
    del(ds.attrs[a])
    




