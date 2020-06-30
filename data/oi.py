import numpy
from netCDF4 import Dataset
from netCDF4 import date2num

def write_output(output_path, data_list, lats, lons, time_list, data_mask_in=None):
    """write the t_interpted output"""
    data = numpy.asarray(data_list)
    ntime = data.shape[0]
    nlat = data.shape[1]
    nlon = data.shape[2]

    rootgrp = Dataset(output_path, 'w')
    rootgrp.createDimension('time', ntime)
    rootgrp.createDimension("south_north", nlat)
    rootgrp.createDimension("west_east", nlon)

    lat = rootgrp.createVariable(
        "latitude", "f4", ("south_north", 'west_east',))
    lon = rootgrp.createVariable(
        "longitude", "f4", ("south_north", 'west_east',))
    t = rootgrp.createVariable(
        "time", "double", ("time", ))
    fcst = rootgrp.createVariable('forecast', 'f4',
            ('time', 'south_north', 'west_east'))
    if data_mask_in is not None:
        data_mask = rootgrp.createVariable(
            'data_mask', 'f4', ('south_north', 'west_east'))

    rootgrp.description = "RainCAST t_interp forecasts"
    rootgrp.source = "NZ MetService"

    lat[:, :] = lats
    lat.description = "latitude"
    lat.units = "degree"

    lon[:, :] = lons
    lon.description = "longitude"
    lon.units = "degree"

    fcst[:, :, :] = data
    fcst.description = 'RainCAST t_interp forecasts'
    fcst.units = 'mm/h'
    fcst.coordinates = 'time lat lon'

    calendar = 'gregorian'
    units = 'seconds since 1970-01-01 00:0:0'
    for i in range(ntime):
        t[i] = date2num(time_list[i], calendar=calendar, units=units)
    t.long_name = 'time'
    t.standard_name = 'time'
    t.units = units
    t.axis = 'T'
    t.calendar = calendar

    if data_mask_in is not None:
        data_mask[:, :] = data_mask_in
        data_mask.description = 'data mask'
    rootgrp.close()
