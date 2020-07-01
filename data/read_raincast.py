from netCDF4 import Dataset, num2date

def read_raincast(raincast_path, prob_index=0):
    with Dataset(raincast_path) as cur_nc:
        forecasts = cur_nc.variables['forecast'][prob_index, :, :, :]
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

    forecasts_list = []
    for i in range(forecasts.shape[0]):
        forecasts_list.append(forecasts[i, :, :])

    return forecasts_list, data_mask, latitude, longitude, valid_times

def read_obs(obs_path):
    """read radar data produced from raincast"""

    with Dataset(obs_path) as cur_nc:
        radar = cur_nc.variables['radar'][-1, :, :]
        data_mask = cur_nc.variables['radar'][-1, :, :]
        longitude_radar = cur_nc.variables['longitude'][:]
        latitude_radar = cur_nc.variables['latitude'][:]
        time = cur_nc.variables['time'][:]
        calendar = 'gregorian'
        units = 'seconds since 1970-01-01 00:0:0'
        tradar = num2date(time[-1], units=units,
                     calendar=calendar)
    
    return [radar], data_mask, latitude_radar, longitude_radar, [tradar]
    