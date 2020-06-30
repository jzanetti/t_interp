from data import read_raincast
from data import read_interp

def read_data(data_path, datatype):
    """read different raw data based on datatype"""
    
    if datatype == 'raincast_det':
        forecasts, data_mask, latitude, longitude, valid_times = \
            read_raincast.read_raincast(data_path)
    else:
        raise Exception('to be implemented')
    
    return forecasts, data_mask, latitude, longitude, valid_times

def read_interp_data(data_path, datatype):
    """read interp data"""
    if datatype == 'raincast_det':
        forecast, forecast_times, latitude, longitude, data_mask = \
            read_interp.read_interp_data(data_path)
    else:
        raise Exception('to be implemented')

    return forecast, forecast_times, latitude, longitude, data_mask
    
    
    