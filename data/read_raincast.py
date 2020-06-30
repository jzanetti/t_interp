from netCDF4 import Dataset, num2date

def read_raincast(raincast_path):
    with Dataset(raincast_path) as cur_nc:
        forecasts = cur_nc.variables['forecast'][:]
        longitude = cur_nc.variables['longitude'][:]
        latitude = cur_nc.variables['latitude'][:]
        data_mask = cur_nc.variables['data_mask'][:]        
        valid_times = []
        time = cur_nc.variables['time'][:]
        calendar = 'gregorian'
        units = 'seconds since 1970-01-01 00:0:0'
        for t in range(len(time)):
            valid_times.append(num2date(
                time[t], units=units,
                calendar=calendar))
    
    return forecasts, data_mask, latitude, longitude, valid_times

def read_obs(obs_paths=None):
    radars = []
    radar_times = []
    longitude_radar = None
    latitude_radar = None
    data_mask = None
    if obs_paths is not None:
        for radartime in obs_paths:
            with Dataset(obs_paths[radartime]) as cur_nc:
                radar = cur_nc.variables['radar'][-1, :, :]
                data_mask = cur_nc.variables['radar'][-1, :, :]
                longitude_radar = cur_nc.variables['longitude'][:]
                latitude_radar = cur_nc.variables['latitude'][:]
                time = cur_nc.variables['time'][:]
                calendar = 'gregorian'
                units = 'seconds since 1970-01-01 00:0:0'
                tradar = num2date(time[-1], units=units,
                             calendar=calendar)
                radar_times.append(tradar)
                radars.append(radar)
    
    return radars, radar_times, longitude_radar, latitude_radar, data_mask
    