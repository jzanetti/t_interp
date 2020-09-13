import numpy
from copy import deepcopy
from data import read_raincast
from data import read_qpe
from data import read_interp
from data import regrid


def sort_datapath_based_on_priority(datapath_config):
    """sort data path based on priority"""
    sorted_dicts = sorted(
        datapath_config.items(), 
        key = lambda x: x[1]['priority'], 
        reverse=False)
    
    datapath_list = []
    for sorted_dict in sorted_dicts:
        datapath_list.append(
            sorted_dict[1])
    
    return datapath_list
    

def overwrite_data_using_priority(
        valid_times, data_list,
        valid_times0, data_list0):
    """over write data:
        since we rank the data using priority before, 
        the later arrived one (with higher priority) 
        would overwrite the earlier one"""
    for i, valid_time in enumerate(valid_times):
        if valid_time in valid_times0:
            t_index = valid_times0.index(valid_time)
            data_list0[t_index] = data_list[t_index]
        else:
            valid_times0.append(valid_time)
            data_list0.append(data_list[i])
    
    return valid_times0, data_list0


def check_latlon(lat0, lon0, lat1, lon1, r=0.01):
    """check if lat0/lon0 are consistent with lat1/lon1"""
    if numpy.max(abs(lat0 - lat1)) > r or \
        numpy.max(abs(lon0 - lon1)) > r:
        raise Exception('src data have different coordinates')


def get_ref_latlon(lat, lon):
    return deepcopy(lat), deepcopy(lon)


def get_input_data(data_in, lat_in, lon_in, area_spcifications):
    src_grid = {'lat': lat_in, 'lon': lon_in, 'data': data_in}
    cur_area_lat_start = area_spcifications['lats'][1]
    cur_area_lat_end = area_spcifications['lats'][0]

    cur_area_lon_start = area_spcifications['lons'][0]
    cur_area_lon_end = area_spcifications['lons'][1]
    
    target_res_dg = area_spcifications['res']
    cur_area_lat0 = numpy.arange(
        cur_area_lat_start, cur_area_lat_end, target_res_dg)
    cur_area_lat_size = int(int(len(cur_area_lat0)/10.0)*10.0)
    cur_area_lat = cur_area_lat0[0:cur_area_lat_size]

    cur_area_lon0 = numpy.arange(
        cur_area_lon_start, cur_area_lon_end, target_res_dg)
    cur_area_lon_size = int(int(len(cur_area_lon0)/10.0)*10.0)
    cur_area_lon = cur_area_lon0[0:cur_area_lon_size]

    lon_out, lat_out = numpy.meshgrid(cur_area_lon, cur_area_lat)
    
    lon_out = lon_out % 360.0
    tar_grid = {'lat': lat_out, 'lon': lon_out}
    
    data_out = regrid.grid_interpolation(src_grid, tar_grid)
    
    return data_out, lat_out, lon_out


def read_data(data_path):
    """read different raw data based on datatype"""
    
    datapath_list = sort_datapath_based_on_priority(
        data_path['data_src'])
    
    data_list0 = []
    valid_times0 = []
    for i, datapath in enumerate(datapath_list):
        try:
            if datapath['type'] == 'raincast_det':
                data_list, data_mask, latitude, longitude, valid_times = \
                    read_raincast.read_raincast(datapath['src'], prob_index=0)
            elif datapath['type'] == 'raincast_radar':
                data_list, data_mask, latitude, longitude, valid_times = \
                    read_raincast.read_obs(datapath['src'])
            elif datapath['type'] == 'qpe':
                data_list, data_mask, latitude, longitude, valid_times = \
                    read_qpe.read_qpe(datapath['src'])
        except FileNotFoundError:
            continue
         
        if i == 0:
            ref_lat, ref_lon = get_ref_latlon(latitude, longitude)
        
        check_latlon(latitude, longitude, ref_lat, ref_lon)
        valid_times0, data_list0 = overwrite_data_using_priority(
            valid_times, data_list,
            valid_times0, data_list0)
    
    ftime_list = sorted(valid_times0)
    fdata_list = [x for _,x in sorted(zip(valid_times0, data_list0))]
    
    if data_path['grid'] is not None:
        fdata_list_new = []
        for fdata in fdata_list:
            f_data_new, latitude_new, longitude_new = \
                get_input_data(fdata, latitude, longitude, data_path['grid'])
            fdata_list_new.append(f_data_new)
        forecasts = numpy.asarray(fdata_list_new)
        return forecasts, data_mask, latitude_new, longitude_new, ftime_list
    
    
    forecasts = numpy.asarray(fdata_list)    
    return forecasts, data_mask, latitude, longitude, ftime_list


def read_interp_data(data_path):
    """read interp data"""
    forecast, forecast_times, latitude, longitude, data_mask = \
        read_interp.read_interp_data(data_path)

    return forecast, forecast_times, latitude, longitude, data_mask

    
    