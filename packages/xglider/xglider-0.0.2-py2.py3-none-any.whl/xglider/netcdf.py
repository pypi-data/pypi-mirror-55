# Licensed under Apache Software License style license - see LICENSE

"""Saves xglider datasets as netCDF
   It follows the Discrete Sampling Geometries of CF standards
"""

from collections import OrderedDict
import copy
from datetime import datetime
import json
import pkg_resources
import os.path
from os.path import expanduser

import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import MultiPoint
import netCDF4


# remove NaN along dimensions
# global_attributes
# id_attribute
# ds.sortby(['mission_name', 'profile', 'depth'])


def xgliderrc(subdir=None):
    """Returns the directory with custom config for Xglider
    """
    path = expanduser(os.getenv('XGLIDER_DIR', '~/.config/xgliderrc'))
    if subdir is not None:
        path = os.path.join(path, subdir)
    return path


def inheritance(child, parent):
    """Aggregate into child what is missing from parent
    """
    for v in child:
        if (v in parent) and isinstance(child[v], dict) and isinstance(parent[v], dict):
            parent[v] = inheritance(child[v], parent[v])
        else:
            parent[v] = child[v]
    return parent


def load_cfg(cfgname):
    """Load a config json file from package or user custom
    """
    assert type(cfgname) in (OrderedDict, dict, str), \
            'cfgname must be a dictionary or a str'

    if isinstance(cfgname, dict):
        cfg = OrderedDict(copy.deepcopy(cfgname))
    elif type(cfgname) is str:
        path = os.path.join('netcdf_cfg', '{}.json'.format(cfgname))
        try:
            cfg = json.loads(pkg_resources.resource_string('xglider', path),
                             object_pairs_hook=OrderedDict)
        except:
            path = os.path.join(xgliderrc(), path)
            cfg = json.load(open(path, 'r'), object_pairs_hook=OrderedDict)
    else:
        return

    if 'inherit' in cfg:
        if isinstance(cfg['inherit'], str):
            cfg['inherit'] = [cfg['inherit']]
        for parent in cfg['inherit']:
            cfg = inheritance(cfg, load_cfg(parent))

    return cfg


def _apply_variables_standard(cfg):
    if 'variables_standard' not in cfg:
        return cfg

    if 'attrs' not in cfg['variables_standard']:
        return cfg

    for v in cfg['variables']:
        attrs = cfg['variables_standard']['attrs'].copy()
        if 'attrs' in cfg['variables'][v]:
                for a in cfg['variables'][v]['attrs']:
                    attrs[a] = cfg['variables'][v]['attrs'][a]
        cfg['variables'][v]['attrs'] = attrs

    return cfg

def set_default_attributes(ds, cfgname, dropna=True):
    """
    """
    cfg = load_cfg(cfgname)

    ds = ds.copy(deep=True)

    if 'global_attributes' in cfg:
        attrs = cfg['global_attributes']
        for a in ds.attrs:
            attrs[a] = ds.attrs[a]
        ds.attrs = attrs

    if ('variables_standard' in cfg) and ('attrs' in cfg['variables_standard']):
        for v in cfg['variables']:
            attrs = cfg['variables_standard']['attrs'].copy()
            if 'attrs' in cfg['variables'][v]:
                for a in cfg['variables'][v]['attrs']:
                    attrs[a] = cfg['variables'][v]['attrs'][a]
            cfg['variables'][v]['attrs'] = attrs

    if 'variables' in cfg:
        for v in cfg['variables']:
            if v in ds.variables:
                if ('attrs' in cfg['variables'][v]):
                    attrs = cfg['variables'][v]['attrs']
                    for a in ds[v].attrs:
                        if (a not in attrs) or (ds[v].attrs[a] is not None):
                            attrs[a] = ds[v].attrs[a]
                    ds[v].attrs = attrs
                if ('encoding' in cfg['variables'][v]):
                    for e in cfg['variables'][v]['encoding']:
                        ds[v].encoding[e] = cfg['variables'][v]['encoding'][e]
                if 'varname' in cfg['variables'][v]:
                    ds = ds.rename({v: cfg['variables'][v]['varname']})

    if dropna is True:
        for a in [a for a in ds.attrs if ds.attrs[a] is None]:
            del(ds.attrs[a])

        for v in ds.variables:
            for a in [a for a in ds[v].attrs if ds[v].attrs[a] is None]:
                del(ds[v].attrs[a])

    return ds


def set_time_attributes(ds):
    """Set time coverage global attributes

       Based on input content, define the time coverage attributes as
         recommended by CF.
    """
    ds = ds.copy(deep=True)

    time_vars = [v for v in ds.coords if ds[v].dtype == 'datetime64[ns]']
    time = pd.Series()
    for v in time_vars:
        time = time.append(ds[v].to_series())

    ds.attrs['time_coverage_start'] = pd.to_datetime(
            time.min()).strftime("%Y-%m-%dT%H:%M:%SZ")
    ds.attrs['time_coverage_end'] = pd.to_datetime(
            time.max()).strftime("%Y-%m-%dT%H:%M:%SZ")

    return ds


def set_geospatial_attributes(ds, mode='EPSG:4326'):
    """Set geospatial global attributes

       Based on input content, define the geospatial attributes as
         recommended by CF.

       ATENTION: Allow some flexibility with lat/lon varnames.
    """
    assert ('lat' in ds.coords) and ('lon' in ds.coords), \
            "For now I'm hard coded for lat/lon."

    ds = ds.copy(deep=True)

    ds.attrs['geospatial_bounds_crs'] = mode

    latlon = np.stack((ds.lat.values, ds.lon.values), axis=1)
    latlon = latlon[~np.isnan(latlon).any(axis=1)].tolist()
    points = MultiPoint(latlon)

    # ds.attrs['geospatial_bounds'] = points.envelope.wkt
    ds.attrs['geospatial_bounds'] = points.convex_hull.wkt
    ds.attrs['geospatial_lat_min'], ds.attrs['geospatial_lat_max'], \
    ds.attrs['geospatial_lon_min'], ds.attrs['geospatial_lon_max'] = \
    points.bounds

    if 'depth' in ds:
        ds.attrs['geospatial_vertical_min'] = int(np.floor(ds.depth.min()))
        ds.attrs['geospatial_vertical_max'] = int(np.ceil(ds.depth.max()))

    return ds


def convert_datetime2seconds(ds):
    """Convert datetime variables into seconds since

       This is a temporary solution. There are better ways to do this.
    """
    for v in ds.variables:
        if ds[v].dtype.str in ('<M8[ns]'):
            attrs = ds[v].attrs
            ds[v] = (ds[v] - np.datetime64('1970-01-01T00:00:00')) \
                / np.timedelta64(1, 's')
            ds[v].attrs['standard_name'] = 'time'
            ds[v].attrs['long_name'] = "Time"
            ds[v].attrs['units'] = "seconds since 1970-01-01T00:00:00Z"
            ds[v].attrs['axis'] = "T"
            ds[v].attrs['calendar'] = "gregorian"
            for a in [a for a in attrs if a not in ds[v].attrs]:
                ds[v].attrs[a] = attrs[a]

    return ds


def mission2trajectory_index(ds):
    """
    """
    assert 'mission_name' not in ds

    ds = ds.copy(deep=True)

    trajectories = sorted(set(ds.mission.data))
    trajectories_index = [trajectories.index(m) for m in ds.mission.values]

    attrs = ds.mission.attrs.copy()
    ds['trajectory_index'] = xr.DataArray(trajectories_index, dims=ds.mission.dims)
    ds.trajectory_index.attrs['long_name'] = "which mission (trajectory) this profile is part of"
    # ds.trajectory_index.attrs['instance_dimension'] = "mission"
    ds.trajectory_index.attrs['comment'] = "This dataset combines several underwater glider missions, i.e. several deployments. Profiles originated from the same mission have the same trajectory_index number. The names of the missions can be obtained from the variable mission_name, so that trajectory_index=0 relates to the first item in the variable mission_name."
    ds.trajectory_index.attrs['ancillary_variables'] = "mission_name"
    ds = ds.set_coords('trajectory_index')

    ds['mission'] = ds.trajectory_index
    ds.mission.attrs['comment'] = "ATTENTION, please use trajectory_index instead. - " +  ds.trajectory_index.attrs['comment']
    ds = ds.set_coords('mission')

    # if 'long_name' not in attrs:
    attrs['long_name'] = "Mission name of each trajectory."
    # if 'comment' not in attrs:
    attrs['comment'] = "Mission name related to the variable trajectory_index, so that every record (profile) with trajectory_index=0 is related to the first name recorded here (mission_name), trajectory_index=1 related to second name record, and so on. The individual trajectories (missions) are also available in separated files with the same name (mission) used here."
    ds['mission_name'] = xr.DataArray(
            trajectories,
            dims=('trajectory',))
    for a in attrs:
        ds['mission_name'].attrs[a] = attrs[a]
    ds = ds.set_coords('mission_name')

    return ds


def netcdf3_safe_dtypes(ds):
    """Fix dtypes for netCDF3 restrictions

       NetCDF-3 doesn't accept some data types, so modify it to the closest
         possible, for example, it converts unsigned int to int.
    """
    ds = ds.copy(deep=True)

    for v in [v for v in ds.variables if ds[v].dtype.kind == 'u']:
        tmp = ds[v].astype(ds[v].dtype.str.replace('u', 'i'))
        for a in ds[v].attrs:
            tmp.attrs[a] = ds[v].attrs[a]
        for e in ds[v].encoding:
            tmp.encoding[e] = ds[v].encoding[e]
        ds[v] = tmp

    for v in [v for v in ds.variables if 'i8' in ds[v].dtype.str]:
        tmp = ds[v].astype(ds[v].dtype.str.replace('i8', 'i4'))
        for a in ds[v].attrs:
            tmp.attrs[a] = ds[v].attrs[a]
        for e in ds[v].encoding:
            tmp.encoding[e] = ds[v].encoding[e]
        ds[v] = tmp

    return ds


def NGDAC30(ds, path, cfgname=None, format='NETCDF4_CLASSIC'):
    """

       It's a shame that can't achieve the required format using xr.to_netcdf
    """
    trajectory = 'sp022-20170209T1616'

    ds['trajectory'] = xr.DataArray(bytes(trajectory, 'utf-8'))

    if cfgname is not None:
        ds = set_default_attributes(ds, cfgname)

    # ngdac_varnames = {'lat': 'profile_lat', 'lon': 'profile_lon', 'datetime': 'profile_time', 'datetime_uv': 'time_uv', 'temp': 'temperature', 'sal': 'salinity'}
    # ds = ds.rename(ngdac_varnames)

    ds.reset_coords().to_netcdf(path, format=format)

    # ======


def trajectoryProfile_single(ds, path, format='NETCDF4_CLASSIC'):
    """Save a dataset with a single mission as a trajectoryProfile
    """
    ds = ds.copy(deep=True)

    mission = np.unique(ds.mission)
    assert mission.size == 1, \
            "Looks like there is more than one mission on this dataset"
    ds['trajectory'] = mission[0]
    if 'cf_role' not in ds.mission.attrs:
        ds.trajectory.attrs['cf_role'] = "trajectory_id"
    for a in ds.mission.attrs:
        ds.trajectory.attrs[a] = ds.mission.attrs[a]
    ds.set_coords('trajectory')
    del(ds['mission'])

    if format != 'NETCDF4':
        netcdf3_safe_dtypes(ds, inplace=True)

    ds.reset_coords().to_netcdf(path, format=format)


def trajectoryProfile_ragged2D(ds, path, format='NETCDF4_CLASSIC',
                               cfgname=None):
    """Save a dataset as a ragged trajectory profile (depth x profile)

       Initial prototype from Spray libraries.
    """
    ds = ds.copy(deep=True)

    ds = mission2trajectory_index(ds)

    # date created
    if ('date_created' not in ds.attrs) or (ds.attrs['date_created'] is None):
        ds.attrs['date_created'] = datetime.utcnow().\
                                            strftime("%Y-%m-%dT%H:%M:%SZ")

    ds = set_time_attributes(ds)
    ds = set_geospatial_attributes(ds, mode='EPSG:4326')
    ds = convert_datetime2seconds(ds)

    if cfgname is not None:
        ds = set_default_attributes(ds, cfgname, dropna=True)

    if format != 'NETCDF4':
        ds = netcdf3_safe_dtypes(ds)

    # ds.reset_coords().to_netcdf(path, format=format)

    ncout = netCDF4.Dataset(path, mode='w', format='NETCDF4_CLASSIC')

    for v in ds.attrs:
        if ds.attrs[v] is not None:
            setattr(ncout, v, ds.attrs[v])

    # Dimensions
    dims = {}
    dims['depth'] = ncout.createDimension('depth', ds.depth.size)
    dims['profile'] = ncout.createDimension('profile', ds.profile.size)
    name_strlen = max([len(n) for n in ds.mission_name.to_series()])
    dims['name_strlen'] = ncout.createDimension('name_strlen', name_strlen)
    dims['trajectory'] = ncout.createDimension('trajectory',
                                               ds.trajectory.size)

    # Variables
    variables = {}

    variables['profile'] = ncout.createVariable('profile', 'i4', ('profile',))
    variables['profile'].cf_role = "profile_id"
    variables['profile'][:] = ds.profile.values

    variables['mission_name'] = ncout.createVariable('mission_name', 'c',
                                                     ('trajectory',
                                                      'name_strlen'))
#    #variables['mission_name'].cf_role = "trajectory_id"
    for a in ds.mission_name.attrs:
        if ds.mission_name.attrs[a] is not None:
            setattr(variables['mission_name'], a, ds.mission_name.attrs[a])
    mission_name = ds.mission_name.values.tolist()
    variables['mission_name'][:] = [list(d) for d in mission_name]

#    variables['mission'] = ncout.createVariable('mission', 'i4', ('profile',))
#    variables['mission'].long_name = "Mission id"
#    #variables['mission'].cf_role = "trajectory_id"
#    variables['mission'].ancillary_variables = "mission_name"
#    variables['mission'].comment = "This dataset combines several Spray underwater missions, i.e. several deployments. Profiles originated from the same mission have the same mission number. The names of the missions can be obtained from mission_name."
#    variables['mission'][:] = [mission_name.index(m) for m in ds.mission.values]

    # var_order = [v for v in var_order if v in ds]
    # var_order = [v for v in ds.keys() if v not in ncout.variables]
    # for v in var_order:
    for v in [v for v in ds.variables.keys() if v not in ncout.variables]:

        dtype = ds[v].dtype.str.replace('<', '')
        # Coordinates must not have fill_value
        if (v in ds.dims) or (ds[v].dtype.kind == 'i'):
            variables[v] = ncout.createVariable(v,
                                                dtype,
                                                ds[v].dims)
        else:
            variables[v] = ncout.createVariable(v,
                                                dtype,
                                                ds[v].dims,
                                                fill_value=np.nan)
        variables[v][:] = ds[v].values

        for a in ds[v].attrs:
            if ds[v].attrs[a] is not None:
                setattr(variables[v], a, ds[v].attrs[a])

    ncout.close()
