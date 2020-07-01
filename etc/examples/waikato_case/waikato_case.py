import os
import pygrib
import numpy
from datetime import datetime
from datetime import timedelta
from pysteps.postprocessing import probmatching
from netCDF4 import Dataset, num2date
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


WRF_FILENAME = '{model_name}_02_{analysis_time}_{lead_hr}.00.grb'
QPE_COLORMAP = [
    "#fdfdfd",   # 10.00+
    "#04e9e7",  # 0.01 - 0.10 inches
    "#019ff4",  # 0.10 - 0.25 inches
    "#0300f4",  # 0.25 - 0.50 inches
    "#02fd02",  # 0.50 - 0.75 inches
    "#01c501",  # 0.75 - 1.00 inches
    "#008e00",  # 1.00 - 1.50 inches
    "#fdf802",  # 1.50 - 2.00 inches
    "#e5bc00",  # 2.00 - 2.50 inches
    "#fd9500",  # 2.50 - 3.00 inches
    "#fd0000",  # 3.00 - 4.00 inches
    "#d40000",  # 4.00 - 5.00 inches
    "#bc0000",  # 5.00 - 6.00 inches
    "#f800fd",  # 6.00 - 8.00 inches
    "#9854c6",  # 8.00 - 10.00 inches
]
QPE_COLORMAP = matplotlib.colors.ListedColormap(QPE_COLORMAP)
QPE_CLEVS = {
    #60: [0.00, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.5, 5.0, 7.5, 10.0, 15.0,
    #          20.0, 30.0, 40.0, 50.0],
    60: [0.0, 0.2, 0.5, 0.75, 1.0, 1.5, 2.5, 3.0, 5.0, 7.5, 10.0, 15.0,
           20.0, 30.0, 40.0, 50.0],
    180: [0.00, 0.2, 1.0, 2.0, 5.0, 10.0, 15.0, 25.0, 35.0, 50.0, 75.0, 90.0,
              120.0, 150.0, 180.0, 220.0],
    1440: [0.00, 0.05, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0,
              45.0, 50.0, 55.0, 60.0]
    }

def generate_plot(lat, lon, data, model_name, analysis_time,
                  valid_time, filename_to_save,
                  llcrnrlon=None, urcrnrlon=None, llcrnrlat=None, urcrnrlat=None):
    
    if llcrnrlon is None:
        llcrnrlon=lon.min()
    if urcrnrlon is None:
        urcrnrlon=lon.max()
    if llcrnrlat is None:
        llcrnrlat=lat.min()
    if urcrnrlat is None:
        urcrnrlat=lat.max()

    fig = plt.figure(figsize=(12, 12))
    levels = QPE_CLEVS[60]
    norm = matplotlib.colors.BoundaryNorm(levels, 15)
    m = Basemap(
        projection='mill', llcrnrlon=llcrnrlon,
        urcrnrlon=urcrnrlon, llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
        resolution='i')

    x, y = m(lon, lat)
    cs = m.contourf(x, y, data, norm=norm, levels=levels,
                    cmap=QPE_COLORMAP, shading='gouraud')

    m.drawcoastlines()
    m.drawmapboundary()
    plt.colorbar(cs, orientation='horizontal', fraction=0.05, pad=0.04)
    plt.title('{model_name}, analysis time: {analysis_time} \n accumulation '
              'period: {valid_time}'.format(
                    model_name=model_name,
                    analysis_time=analysis_time, valid_time=valid_time))
    plt.savefig('/tmp/{}'.format(filename_to_save), bbox_inches='tight')
    plt.close()



def plot_wrfpp(start_datetime, end_datetime, analysis_time, model_name, wrf_dir):

    valid_time = start_datetime
    
    while valid_time <= end_datetime:
        print('start processing {}'.format(valid_time))
        lead_hr = int((valid_time - analysis_time).total_seconds()/3600.0)

        wrf_filename_list = []
        for cur_lead_hr in [lead_hr-1, lead_hr]:
            
            wrf_filename = WRF_FILENAME.format(
                model_name=model_name,
                analysis_time=analysis_time.strftime('%y%m%d%H'),
                lead_hr=str(cur_lead_hr).zfill(3))
            wrf_path = os.path.join(
                wrf_dir, wrf_filename)
            wrf_filename_list.append(wrf_path)
        
        try:
            grbs_start = pygrib.open(wrf_filename_list[0])
            grbs_end = pygrib.open(wrf_filename_list[1])
        except (FileNotFoundError, OSError):
            valid_time += timedelta(seconds=3600.0)
            continue
    
        grb_start = grbs_start.select(name='Total Precipitation')[0]
        grb_end = grbs_end.select(name='Total Precipitation')[0]
        data_start = grb_start.values
        grb_end = grb_end.values
        data = grb_end - data_start
        lat, lon = grb_start.latlons()
        data[data < 0.05] = numpy.NaN
        data = numpy.ma.array(data, mask=numpy.isnan(data))
    
        lon = lon % 360.0

        generate_plot(
            lat, lon, data, model_name, analysis_time,
            valid_time, '{model_name}_{valid_time}.png'.format(
                model_name=model_name,
                valid_time=valid_time.strftime('%Y%m%d%H%M')),
            llcrnrlon=172, urcrnrlon=180, llcrnrlat=-40.0, urcrnrlat=-35.0)
        valid_time += timedelta(seconds=3600.0)


def plot_raincast_det(start_datetime, end_datetime, analysis_time,
                      raincast_det_path, radar_path):

    raincast_valid_times = []

    with Dataset(raincast_det_path) as cur_nc:
        raincast = cur_nc.variables['forecast'][:]
        latitude = cur_nc.variables['latitude'][:]
        longitude = cur_nc.variables['longitude'][:]
        data_mask = cur_nc.variables['data_mask'][:]
        time = cur_nc.variables['time'][:]
        calendar = 'gregorian'
        units = 'seconds since 1970-01-01 00:0:0'
        for t in range(len(time)):
            raincast_valid_times.append(num2date(
                time[t], units=units,
                calendar=calendar))
            
    radar_valid_times = []
    with Dataset(radar_path) as cur_nc:
        radar = cur_nc.variables['forecast'][:]
        latitude = cur_nc.variables['latitude'][:]
        longitude = cur_nc.variables['longitude'][:]
        data_mask = cur_nc.variables['data_mask'][:]
        time = cur_nc.variables['time'][:]
        calendar = 'gregorian'
        units = 'seconds since 1970-01-01 00:0:0'
        for t in range(len(time)):
            radar_valid_times.append(num2date(
                time[t], units=units,
                calendar=calendar))

    valid_time = start_datetime
    while valid_time <= end_datetime:
        print('raincast_det: start processing {}'.format(valid_time))
        t_index0 =  raincast_valid_times.index(valid_time)
        raincast_data = raincast[t_index0, :, :]

        t_index1 =  radar_valid_times.index(valid_time)
        radar_data = radar[t_index1, :, :]
        
        raincast_data[numpy.isnan(raincast_data)] = 0.0
        radar_data[numpy.isnan(radar_data)] = 0.0
        raincast_data = probmatching.nonparam_match_empirical_cdf(
            raincast_data, radar_data)

        longitude = longitude % 360.0

        generate_plot(
            latitude, longitude, raincast_data, 'raincast', analysis_time,
            valid_time, '{model_name}_{valid_time}.png'.format(
                model_name='raincast',
                valid_time=valid_time.strftime('%Y%m%d%H%M')),
            llcrnrlon=172, urcrnrlon=180, llcrnrlat=-40.0, urcrnrlat=-35.0)
        generate_plot(
            latitude, longitude, radar_data, 'radar', analysis_time,
            valid_time, '{model_name}_{valid_time}.png'.format(
                model_name='radar',
                valid_time=valid_time.strftime('%Y%m%d%H%M')),
            llcrnrlon=172, urcrnrlon=180, llcrnrlat=-40.0, urcrnrlat=-35.0)
        valid_time += timedelta(seconds=600.0)


if __name__ == '__main__':
    start_datetime = '202006292100'
    end_datetime = '202006300100'
    obs_datetime_start = '202006292100'
    obs_datetime_end = '202006292200'
    analysis_time = '202006291200'
    analysis_time_raincast = '202006292200'

    start_datetime = datetime.strptime(start_datetime, '%Y%m%d%H%M')
    end_datetime = datetime.strptime(end_datetime, '%Y%m%d%H%M')
    analysis_time = datetime.strptime(analysis_time, '%Y%m%d%H%M')
    analysis_time_raincast = datetime.strptime(
        analysis_time_raincast, '%Y%m%d%H%M')
    
    wrf_dir = '/home/szhang/Downloads'
    raincast_det_path = '/tmp/t_interp/output/raincast_from_202006292100_to_202006301000.nc'
    radar_path = '/tmp/t_interp/output/radar_from_202006292100_to_202006300100.nc'
    # plot_raincast_det(start_datetime, end_datetime, analysis_time_raincast,
    #                  raincast_det_path, radar_path)
    plot_wrfpp(start_datetime, end_datetime, analysis_time,
               'nz4kmN-NCEP', wrf_dir)
    
    