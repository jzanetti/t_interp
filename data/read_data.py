import numpy
from copy import deepcopy
from data import read_raincast
from data import read_interp


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

def read_data(data_path):
    """read different raw data based on datatype"""
    
    datapath_list = sort_datapath_based_on_priority(data_path)
    
    data_list0 = []
    valid_times0 = []
    for i, datapath in enumerate(datapath_list):
        if datapath['type'] == 'raincast_det':
            data_list, data_mask, latitude, longitude, valid_times = \
                read_raincast.read_raincast(datapath['src'], prob_index=0)
        elif datapath['type'] == 'raincast_radar':
            data_list, data_mask, latitude, longitude, valid_times = \
                read_raincast.read_obs(datapath['src'])
                
        if i == 0:
            ref_lat, ref_lon = get_ref_latlon(latitude, longitude)
        
        check_latlon(latitude, longitude, ref_lat, ref_lon)
        valid_times0, data_list0 = overwrite_data_using_priority(
            valid_times, data_list,
            valid_times0, data_list0)
    
    ftime_list = sorted(valid_times0)
    fdata_list = [x for _,x in sorted(zip(valid_times0, data_list0))]
    
    forecasts = numpy.asarray(fdata_list)
    return forecasts, data_mask, latitude, longitude, ftime_list

def read_interp_data(data_path):
    """read interp data"""
    forecast, forecast_times, latitude, longitude, data_mask = \
        read_interp.read_interp_data(data_path)

    return forecast, forecast_times, latitude, longitude, data_mask
    
    
    