# -*- coding: utf-8 -*-

"""Module to create plots of gliders.

   Taking advantage of the xglider data object, this module creates standard
     plots.
"""

import os.path

import numpy as np
# import matplotlib
# matplotlib.use('Agg')
from matplotlib import pyplot as plt


def save_all_contours(ds, path='./'):
    figs = all_contours(ds)

    for v in figs:
        fig = figs[v]
        filename = "{0}_{1}.png".format(ds.attrs['short_name'], v)

        f = os.path.join(path, filename)
        fig.savefig(f)
        #fig.close()


def all_contours(ds, xcoord='distance'):
    figs = {}
    varnames = [v for v in ds.keys() if v not in ds.coords]
    varnames = [v for v in varnames if len(ds[v].dims) == 2]
    for v in varnames:
        #fig, ax = plt.subplots()
        fig = plt.figure(figsize=(12,4), dpi=120)
        ax = fig.add_subplot(111)
        try:
            contourf_var(ds, v, ax, xcoord)
            fig.tight_layout()
            figs[v] = fig
        except:
            plt.close(fig)
    return figs


def contourf_var(ds, varname, ax, xcoord=None, dvalues='auto', **kwargs):
    """Contour a single variable
    """
    # cvalues = np.arange(4, 30+1)
    # cticks = np.arange(5, 31, 5)

    # ==== Set xcoord ====
    if xcoord is None:
        assert len(ds[varname].dims) == 2
        assert ds[varname].dims[1] == 'depth'
        xcoord = ds[varname].dims[0]
    if (xcoord == 'distance') and ('units' in ds[xcoord].attrs) and \
            (ds[xcoord].attrs['units'] == 'm'):
                ds = ds.copy(deep=True)
                ds['distance'] *= 1e-3
                ds.distance.attrs['units'] = 'km'
    x = ds[xcoord].data
    if 'long_name' in ds[xcoord].attrs:
        xlabel = ds[xcoord].attrs['long_name']
    elif 'name' in ds[xcoord].attrs:
        xlabel = ds[xcoord].attrs['name']
    else:
        xlabel = ds[xcoord].name
    if 'units' in ds[xcoord].attrs:
        xlabel += " [{0}]".format(ds[xcoord].attrs['units'])
    # ====

    c = ax.contourf(x, ds.depth.data, ds[varname].data.T,
                    extend='both')
    #        cvalues, extend='both')

    if 'xlim' in kwargs:
        assert len(kwargs['xlim']) == 2
        ax.set_xlim(*kwargs['xlim'])

    # Only make sense for distance axis
    # auto rotate so that the left of the plot is S or W
    if xcoord == 'distance':
        dlat = np.diff(ds.lat.quantile([.05, .95]))[0]
        dlon = np.diff(ds.lon.quantile([.05, .95]))[0]
        # Dominant meridional displacement
        profile0 = ds.sel(profile=ds.profile.min())
        if abs(dlon) > abs(dlat):
            if (profile0.lon > ds.lon.mean()).values.all():
                ax.invert_xaxis()
        # Dominant zonal displacement
        else:
            if (profile0.lat > ds.lat.mean()).values.all():
                ax.invert_xaxis()

    ax.set_xlabel(xlabel)
    ax.invert_yaxis()
    ylabel = 'Depth (m)'
    ax.set_ylabel(ylabel)

    #cmap=plt.cm.viridis
    # cbar= plt.colorbar(c, ticks=cticks)
    cbar= plt.colorbar(c, ax=ax)
    if 'long_name' in ds[varname].attrs:
        var_label = ds[varname].attrs['long_name']
    elif 'name' in ds[varname].attrs:
        var_label = ds[varname].attrs['name']
    else:
        var_label = varname
    if 'units' in ds[varname].attrs:
        var_label += " [{0}]".format(ds[varname].attrs['units'])
    # cbar.set_label('Temperature [$^\circ$C]')
    cbar.set_label(var_label)

    # ==== Density layers ====
    if dvalues == 'auto':
        dvalues = np.arange(20, 30.1, 0.25)

        c = ax.contour(x, ds.depth.data, ds.sigma_theta.data.T,
            dvalues, colors='k', alpha=0.3, linewidths=1)
        cs = ax.contour(x, ds.depth.data, ds.sigma_theta.data.T,
            sorted(np.unique(dvalues.astype('i'))), colors='k', linewidths=2)
        ax.clabel(cs, fmt='%i', fontsize=11, inline=True, inline_spacing=10)

    return ax


import oceansdb
import cmocean

def velocityField_depthMean_basemap(ds):

    fig = plt.figure(figsize=(6,6), dpi=120)


    lat_min = float(ds.lat.min())
    lat_max = float(ds.lat.max())
    lat_range = max(0.1, (lat_max - lat_min) * 1.2)
    lat_center = (lat_max + lat_min) / 2.
    lon_min = float(ds.longitude_uv.min())
    lon_max = float(ds.longitude_uv.max())
    lon_range = max(0.1, (lon_max - lon_min) * 1.2)
    lon_center = (lon_max + lon_min) / 2.

    # The shortest axis is at least 2/3 of the longest one
    lon_range = max(lon_range, lat_range * 2./3)
    lat_range = max(lat_range, lon_range * 2./3)

    llcrnrlat = lat_center - lat_range / 2.
    urcrnrlat = lat_center + lat_range / 2.
    llcrnrlon = lon_center - lon_range / 2.
    urcrnrlon = lon_center + lon_range / 2.

    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # lat_ts is the latitude of true scale.
    # resolution = 'c' means use crude resolution coastlines.
    m = Basemap(projection='merc', llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
            llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon,
            lat_ts=20,resolution='h')

    ETOPO = oceansdb.ETOPO()
    subset, dims = ETOPO['topography'].crop(
            var=['height'],
            lon=np.array([llcrnrlon, urcrnrlon]),
            lat=np.array([llcrnrlat, urcrnrlat]))
    lon, lat = np.meshgrid(dims['lon'], dims['lat'])
    xpts, ypts = m(lon, lat)
    cmap = cmocean.cm.deep
    cmap.set_under('0.7')
    cmap.set_over('k')
    m.contourf(
                xpts, ypts, -subset['height'],
                levels=np.arange(0, 5501, 100),
                cmap=cmap, extend='both')

    m.colorbar(ticks=[0, 500, 1000, 2000, 3000, 4000, 5000])

    m.drawcoastlines()
    m.fillcontinents(color='0.7')

    # draw parallels and meridians.
    m.drawparallels(np.arange(-90., 91., 1.), labels=[1, 0, 0, 0], color='0.4',
                    dashes=(None, None), alpha=0.7, zorder=1)
    m.drawmeridians(np.arange(-180., 181., 1.), labels=[0, 1, 0, 1],
                    color='0.4', dashes=(None, None), alpha=0.7, zorder=1)
    v_ref = ds.u_depth_mean.to_series().append(ds.u_depth_mean.to_series()).\
            dropna().abs().quantile(.98)
    scale = v_ref * 8 / 6
    m.quiver([llcrnrlon + lon_range / 10.], [urcrnrlat - lat_range / 10.],
            [.25], [0],
            latlon=True,
            scale_units='inches', scale=scale, width=.0025,
            zorder=2)
    #plt.annotate('25 cm/s',
    #        [llcrnrlon + lon_range / 10., urcrnrlat - lat_range / 10.])
    m.quiver(ds.longitude_uv.data, ds.latitude_uv.data,
            ds.u_depth_mean, ds.v_depth_mean,
            latlon=True,
            scale_units='inches', scale=scale, width=.0025,
            zorder=2)

    #m.drawmapboundary(fill_color='aqua')
    #plt.title("Mercator Projection")

    #fig.tight_layout()

    return fig

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def velocityField_depthMean(ds):
    lon_min = float(ds.lon.min())
    lon_max = float(ds.lon.max())
    lon_c = (lon_max + lon_min)/2.
    lon_range = lon_max - lon_min
    lat_min = float(ds.lat.min())
    lat_max = float(ds.lat.max())
    lat_c = (lat_max + lat_min)/2.
    lat_range = lat_max - lat_min

    min_range = max(1, lon_range, lat_range) * 0.70
    lon_range = max(min_range, lon_range) * 1.15
    lat_range = max(min_range, lat_range) * 1.15

    lon_start = lon_c - lon_range/2.
    lon_end = lon_c + lon_range/2.
    lat_start = lat_c - lat_range/2.
    lat_end = lat_c + lat_range/2.

    fig = plt.figure(figsize=(8, 8), dpi=120)
    ax = plt.axes([0.06, 0.05, 0.86, 0.9], projection=ccrs.PlateCarree())

    ax.set_extent([lon_start, lon_end, lat_start, lat_end],
                  crs=ccrs.PlateCarree())

    ETOPO = oceansdb.ETOPO()
    subset, dims = ETOPO['topography'].crop(
        lon=np.array([lon_start, lon_end]),
        lat=np.array([lat_start, lat_end]),
        var=['height'])
    cmap = cmocean.cm.deep
    cmap.set_under('0.7')
    cmap.set_over('k')
    im = ax.contourf(dims['lon'], dims['lat'], -subset['height'],
                     levels=np.arange(0, 5001, 100),
                     cmap=cmap, extend='both',
                     transform=ccrs.PlateCarree())

    cax = fig.add_axes([0.05, 0.038, 0.86, 0.025])
    plt.colorbar(im, orientation="horizontal",
                 # pad=0.2,
                 # aspect=50,
                 cax=cax,
                 ticks=[0, 500, 1000, 2000, 3000, 4000, 5000])

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, alpha=0.3)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 8, 'weight': 'normal'}
    gl.ylabel_style = {'size': 8, 'weight': 'normal'}

    #ax.set_xticks([-125, -124, -123, -122], crs=ccrs.PlateCarree())
    #ax.set_yticks([35, 36, 37], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
    states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='10m',
            facecolor='none')

    ax.coastlines(resolution='10m', color='black')

    ax.plot(
            ds.reset_coords()['lon'].to_series(),
            ds.reset_coords()['lat'].to_series(),
            '.',
            markersize=1, color='#ff6633', alpha=0.6)

    ax.quiver(
            ds.reset_coords()['lon'].to_series(),
            ds.reset_coords()['lat'].to_series(),
            ds.reset_coords()['u_depth_mean'].to_series(),
            ds.reset_coords()['v_depth_mean'].to_series(),
            color='#ff6633'
            )

    return fig

#from SprayTools.matlab import SprayMatfile
#filename = '/Users/castelao/work/Spray/data/mat/16B01101.mat'
#data = SprayMatfile(filename)

#ds = data['bindata']

#import xarray as xr
#ds = xr.open_dataset('/Users/castelao/work/Spray/data/15C00601.nc')


def fig2rgba(ds):
    fig = contour_temperature(ds)
    fig.canvas.draw()
    #fig.set_tight_layout(True)
    w, h = fig.canvas.get_width_height()
    rgba = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    fig.clear()
    rgba = rgba.reshape(h, w, 4)
    rgba = np.roll(rgba, 3, axis=2)
    #plt.imshow(rgba)
    #plt.show()
    return rgba
