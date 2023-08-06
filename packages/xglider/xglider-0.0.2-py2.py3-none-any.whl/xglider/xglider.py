# -*- coding: utf-8 -*-

"""Main module."""


import numpy as np
from pyproj import Geod
import xarray as xr


def convert_missionObs2profileObs(ds):
    """ Add new dimension groupping observations per profile

        For example, temp(mission, obs) is reorganized into
          temp(mission, profile, obs)
    """
    assert 'profile_id' in ds
    varnames = [v for v in ds if sorted(ds[v].dims) == ['mission', 'obs']]

    tmp = ds[varnames].to_dataframe()

    if 'mission_obs' in tmp:
        tmp = tmp.reset_index('obs', drop=True)
    else:
        tmp = tmp.reset_index('obs').rename(index=str,
                                            columns={'obs': 'mission_obs'})
    tmp = tmp.rename(index=str, columns={'profile_id': 'profile'}).\
              set_index('profile', append=True)
    #tmp = tmp.rename(index=str, columns={'profile_id': 'profile'}).set_index('profile', append=True)
    # tmp['profile'] = tmp.profile_id
    # tmp = tmp.set_index('profile', append=True)
    # tmp['obs'] = tmp.groupby('profile')['mission_obs'].apply(lambda x: x-x.min())
    tmp['obs'] = tmp.groupby(['mission', 'profile'])['mission_obs'].\
                     rank().astype('i')
    tmp = tmp.set_index('obs', append=True)
    tmp = tmp.to_xarray()

    ds = ds.rename({'obs': 'tmp'})
    ds['obs'] = tmp['obs']
    for c in tmp.coords:
        if c not in ds:
            ds[c] = tmp[c]
    for v in tmp:
        ds[v] = tmp[v]

    ds = ds.set_coords('mission_obs')
    ds = ds.drop(['profile_id', 'tmp'])

    return ds


def convert_missionObs2diveObs(ds):
    """ Add new dimension groupping observations per dive

        For example, temp(mission, obs) is reorganized into
          temp(mission, dive, obs)
    """
    assert 'dive_id' in ds

    varnames = [v for v in ds if sorted(ds[v].dims) == ['mission', 'obs']]
    tmp = ds[varnames].to_dataframe()

    if 'mission_obs' in tmp:
        tmp = tmp.reset_index('obs', drop=True)
    else:
        tmp = tmp.reset_index('obs').rename(index=str,
                                            columns={'obs': 'mission_obs'})

    tmp['dive'] = tmp.dive_id
    tmp = tmp.set_index('dive', append=True)
    tmp['obs'] = tmp.groupby('dive')['mission_obs'].apply(lambda x: x-x.min())
    tmp = tmp.set_index('obs', append=True)
    tmp = tmp.to_xarray()

    ds = ds.rename({'obs': 'tmp'})
    ds['obs'] = tmp['obs']
    for c in tmp.coords:
        if c not in ds:
            ds[c] = tmp[c]
    for v in tmp:
        ds[v] = tmp[v]

    ds = ds.drop(['dive_id', 'tmp'])

    return ds


def convert_profileObs2missionObs(ds):
    """
        The current problem is that if one of the variables has an extra
         dimension, let's say fl_unbias with f0_method, all the variables
         will absorb that extra dimension
    """
    varnames = [v for v in ds.variables if 'mission' in ds[v].dims]
    varnames = [v for v in varnames if 'profile' in ds[v].dims]
    varnames = [v for v in varnames if 'obs' in ds[v].dims]

    tmp = ds.reset_coords()[varnames].to_dataframe().dropna(how='all')

    shapes = {}
    for v in varnames:
        d = tuple(sorted(ds[v].dims))
        if d not in shapes:
            shapes[d] = []
        shapes[d].append(v)

    ds = ds.rename({'obs': 'tmp'})
    for s in shapes:
        vs = shapes[s] 
        if ('mission_obs' in ds) and ('mission_obs' not in vs):
            vs.append('mission_obs')
        tmp = ds.reset_coords()[vs].to_dataframe().dropna(how='all')

        if 'profile_id' in tmp:
            tmp = tmp.reset_index('profile', drop=True)
        else:
            tmp = tmp.reset_index('profile').rename(columns={'profile': 'profile_id'})
        if 'profile_obs' in tmp:
            tmp = tmp.reset_index('obs', drop=True)
        else:
            tmp = tmp.reset_index('obs').rename(columns={'obs': 'profile_obs'})
        if 'mission_obs' in tmp:
            tmp['obs'] = tmp.mission_obs.astype(int)
            tmp = tmp.sort_values('obs').set_index('obs', append=True)
            tmp = tmp.drop('mission_obs', axis='columns')
        else:
            assert False

        tmp.sort_index(inplace=True)
        tmp = tmp.to_xarray()

        for c in tmp.coords:
            if c not in ds:
                ds[c] = tmp[c]
        for v in tmp:
            ds[v] = tmp[v]

    assert [v for v in ds.variables if 'tmp' in ds[v].dims] == ['tmp']
    ds = ds.drop('tmp')

    return ds

##def convert_profileDepth2
#def squeeze(ds, dim):
#assert 'obs' in ds.dims
#assert dim in ds.dims
#varnames = [v for v in ds.variables if (dim in ds[v].dims) and ('obs' in ds[v].dims)]
#tmp = ds.reset_coords()[varnames]
#
#
#
#
#if len(ds.dims) > 2:
#    extra_dim = [d for d in tmp.dims if d not in ('obs', dim)][0]
#    for grp_name, grp in tmp.groupby(extra_dim):
#        
#
#.to_dataframe().dropna()
##tmp = tmp.reset_index([dim, 'obs']).rename(index=str, columns={'obs': '{}_obs'.format(dim)})
##tmp['obs'] = tmp.mission_obs.astype('i')
##tmp = tmp.set_index('obs', append=True).to_xarray()
##
##
##tmp = tmp.rename(index=str, columns={'obs', '{}_obs'.format(dim)})
#
#
## ds['data'][['dive_id', 'dive_obs', 'depth', 'temp']].to_dataframe().reset_index('obs').set_index(['dive_id', 'dive_obs'], append=True).to_xarray()




def set_distance(ds, inplace=False):
    """From Lat/Lon estimate horizontal distance along path
    """
    assert ('lat' in ds), "Missing lat in dataset"
    assert ('lon' in ds), "Missing lon in dataset"

    if not inplace:
        ds = ds.copy(deep=True)

    g = Geod(ellps='WGS84')
    L = g.inv(ds.lon.values[:-1], ds.lat.values[:-1],
              ds.lon.values[1:], ds.lat.values[1:])[2]
    L = np.append([0], L.cumsum())
    ds['distance'] = xr.DataArray(L, dims='dive')

    ds.distance.attrs['name'] = 'distance'
    ds.distance.attrs['long_name'] = 'Distance along path'
    ds.distance.attrs['units'] = 'm'

    ds.set_coords('distance', inplace=True)

    if not inplace:
        return ds


def Nsquared(ds):
    depth, lat = np.meshgrid(ds.depth, ds.lat)
    pressure = gsw.conversions.p_from_z(-depth, lat)
    ct = gsw.conversions.CT_from_t(ds.sal, ds.temp, pressure)
    N2 = xr.DataArray(gsw.stability.Nsquared(ds.sal, ct, pressure, axis=-1)[0],
                      dims=['profile', 'depth'])


