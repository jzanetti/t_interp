from netCDF4 import Dataset, num2date

def read_qpe(qpe_path):
    with Dataset(qpe_path) as cur_nc:
        qpe = cur_nc.variables['qpe_sat_raw'][0, :, :]
        longitude = cur_nc.variables['lon'][:]
        latitude = cur_nc.variables['lat'][:]   
        time = cur_nc.variables['time'][:]
        calendar = 'gregorian'
        units = 'seconds since 1970-01-01 00:0:0'
        valid_time = num2date(
                time[0], units=units,
                calendar=calendar)

    return [qpe], None, latitude, longitude, [valid_time]