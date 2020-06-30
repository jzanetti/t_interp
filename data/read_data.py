from data import read_raincast

def read_data(data_path, datatype):
    """read different data based on datatype"""
    
    if datatype == 'raincast_det':
        forecasts, data_mask, latitude, longitude, valid_times = \
            read_raincast.read_raincast(data_path)
    else:
        raise Exception('to be implemented')
    
    return forecasts, data_mask, latitude, longitude, valid_times