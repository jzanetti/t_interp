from netCDF4 import Dataset
from netCDF4 import num2date

def read_interp_data(interp_path):
    forecast_times = []
    with Dataset(interp_path) as cur_nc:
        forecast = cur_nc.variables['forecast'][:, :, :]
        try:
            data_mask = cur_nc.variables['data_mask'][:, :]
        except KeyError:
            data_mask = None
        longitude = cur_nc.variables['longitude'][:]
        latitude = cur_nc.variables['latitude'][:]
        time = cur_nc.variables['time'][:]
        calendar = 'gregorian'
        units = 'seconds since 1970-01-01 00:0:0'
        for t in range(len(time)):
            forecast_times.append(num2date(
                time[t], units=units,
                calendar=calendar))
    
    return forecast, forecast_times, latitude, longitude, data_mask