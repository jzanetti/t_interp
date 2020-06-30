
import os
from netCDF4 import Dataset, num2date
from utils import utils
from datetime import timedelta
from interp import temporal_interp
from vis import plot_forecast



raincast_out = '/home/szhang/Downloads/raincast_determinstic_202006292200.nc'
out_dir = '/tmp'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

datatype = 'raincast_det'
interpolated_fcst = []
interpolated_time = []
with Dataset(raincast_out) as cur_nc:
    forecast = cur_nc.variables['forecast'][:]
    longitude = cur_nc.variables['longitude'][:]
    latitude = cur_nc.variables['latitude'][:]
    valid_times = []
    time = cur_nc.variables['time'][:]
    calendar = 'gregorian'
    units = 'seconds since 1970-01-01 00:0:0'
    for t in range(len(time)):
        valid_times.append(num2date(
            time[t], units=units,
            calendar=calendar))


cur_time = min(valid_times)
end_time = max(valid_times)
interval_min = 10

while cur_time <= (min(valid_times) + timedelta(seconds=3600)):
    print(cur_time)
    t_boundary = utils.get_datetime_boundary(valid_times, cur_time)
    if t_boundary is None:
        fcst = utils.extract_raw_img(forecast, valid_times, cur_time, prob_index=1)
        interpolated_time.append(cur_time)
        interpolated_fcst.append(fcst)
        cur_time += timedelta(seconds=60*interval_min)
        continue

    if datatype == 'raincast_det':
        img_boundary = utils.get_raincast_det_img_boundary(
            forecast, t_boundary, valid_times,
            prob_index=1)
    r = temporal_interp.t_interp(t_boundary, img_boundary, cur_time)
    interpolated_time.append(cur_time)
    interpolated_fcst.append(r)
    cur_time += timedelta(seconds=60*interval_min)

for i, fcst in enumerate(interpolated_fcst):
    print(interpolated_time[i])
    plot_forecast.plot_forecasts(
        fcst, latitude, longitude, interpolated_time[i], datatype, out_dir)
    

