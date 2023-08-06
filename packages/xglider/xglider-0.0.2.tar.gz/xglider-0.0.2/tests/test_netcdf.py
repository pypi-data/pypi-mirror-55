#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `xglider.netcdf` module."""

from collections import OrderedDict

import numpy as np
import pytest
import xarray as xr

from xglider import netcdf


# Some default configs
CFG = ['xglider', 'spray']

def test_load_defaults():
    for c in CFG:
        cfg = netcdf.load_cfg(c)

        assert(isinstance(cfg, OrderedDict))


def test_inheritance():

    my_cfg = {"inherit": "spray",
              "variables": {"temp": {"attrs": {"pytest": "passed"}}}}
    cfg = netcdf.load_cfg(my_cfg)

    assert ('pytest' in cfg['variables']['temp']['attrs']), \
            "Didn't aggregate new child item"
    assert (cfg['variables']['temp']['attrs']['pytest'] == 'passed'), \
            "Wrong value from child"


    my_cfg = {"inherit": "spray",
              "variables": {"temp": {"attrs": {"standard_name": "pytest"}}}}
    cfg = netcdf.load_cfg(my_cfg)

    assert (cfg['variables']['temp']['attrs']['standard_name'] == 'pytest'), \
            "Didn't over-write parent with child value"

    my_cfg = {"inherit": "spray",
              "global_attributes": {"pytest": None}}
    # ds = set_default_attributes(ds, my_cfg)


def test_set_default_attributes_local_priority():
    """Test if local attr in Dataset has priority over template

       ATTENTION, implement the same for global attributes
    """
    my_cfg = {"inherit": "spray",
              "variables": {"foo": {"attrs": {"pytest": "failed"}}}}
    cfg = netcdf.load_cfg(my_cfg)

    data = xr.DataArray(np.random.randn(2, 3).astype('u8'),
                            dims=('x', 'y'),
                            coords={'x': [10, 20]})
    data.attrs['pytest'] = "passed"
    ds = netcdf.set_default_attributes(xr.Dataset({'foo': data}), my_cfg)
    assert ds.foo.attrs['pytest'] == "passed"

    # Double check if I'm really testing an over-writting situation
    assert ds.foo.attrs['pytest'] != cfg['variables']['foo']['attrs']['pytest']


def test_netcdf3_safe_dtypes():
    """Check if attrs & encoding are preserved
    """
    long_name = 'random velocity'
    fillvalue = -999

    for t in ('u4', 'u8', 'i8'):
        data = xr.DataArray(np.random.randn(2, 3).astype('u8'),
                            dims=('x', 'y'),
                            coords={'x': [10, 20]})
        data.attrs['long_name'] = long_name
        data.encoding["_FillValue"] = fillvalue
        ds = xr.Dataset({'foo': data})

        tmp = netcdf.netcdf3_safe_dtypes(ds)
        assert('long_name' in tmp.foo.attrs)
        assert(tmp.foo.long_name == long_name)
        assert( hasattr(tmp.foo, 'encoding') )
        assert(tmp.foo.encoding['_FillValue'] == fillvalue)

