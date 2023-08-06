=====
Usage
=====

----------
Data Model
----------

Xglider expects the data to be in certain structure, so all components know how to find what. 


Ragged Array
------------

It's like a time series with continuous observations, usually along one mission (deployment). The main dimension is obs (observation). 
In the case of summary variables, like the representative latitude for a profile, it is used the dimension profile.

::

    Dimensions:           (mission: 1, dive: 1151, obs: 1080434)
    Coordinates:
      * mission           (mission) object '18804001'
      * dive              (dive) uint64 1 2 3 4 5 6 ... 1148 1149 1150 1151
      * obs               (obs) int64 0 1 2 3 4 ... 1080431 1080432 1080433
    Data variables:
        dive_obs          (mission, obs) int64 0 1 2 3 4 5 ... 181 182 183 184
        dive_id           (mission, obs) uint16 1 1 1 1 1 ... 1151 1151 1151
        u_mean            (mission, dive) float64 0.09284 -0.05191 ... -0.05895
        v_mean            (mission, dive) float64 -0.1007 -0.05501 ... -0.0258
        profile_time      (mission, dive) datetime64[ns] 2018-08-16T20:14:08 ... 2018-12-06T17:19:19.250000
        profile_uv_time   (mission, dive) datetime64[ns] 2018-08-16T20:01:32 ... 2018-12-06T17:10:36.500000
        profile_lat       (mission, dive) float64 36.8 36.79 36.79 ... .79 36.79
        profile_uv_lat    (mission, dive) float64 36.8 36.79 36.79 ... .79 36.79
        profile_lon       (mission, dive) float64 -121.9 -121.9 ... 121.8 -121.8
        profile_uv_lon    (mission, dive) float64 -121.9 -121.9 ... 121.8 -121.8
        press             (mission, obs) float64 0.04 0.04 0.04 0.0 ... 2.52 1.6
        depth             (mission, obs) float64 0.0397 0.0397 ... 2.501 1.588
        temp              (mission, obs) float64 nan nan nan ... 14.91 14.91
        sal               (mission, obs) float64 nan nan nan nan ... 33.6 33.6
        fl                (mission, obs) float64 nan nan nan ... 0.576 0.57
        temp_qc           (mission, obs) uint8 9 9 9 9 9 9 9 9 9 ... 0 0 0 0 0 0
        sal_qc            (mission, obs) uint8 9 9 9 9 9 9 9 9 9 ... 0 0 0 0 0 0
        fl_qc             (mission, obs) uint8 9 9 9 9 9 9 9 9 9 ... 7 7 7 7 7 7
        press_qc          (mission, obs) uint8 0 0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0
    Attributes:
        mission:       18804001
        date_created:  2019-06-12T19:59:26
        src_filename:  18804001.mat
        src_checksum:  e214b49347b4e396e446b9c0f69fc1a0
        description:   MD040 18/08:01 MBARI    Deployed by ERG.  Nortek+DO63
        platform_id:   40

----------
Quickstart
----------


To use xglider in a project::

    import xglider
