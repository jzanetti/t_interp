import os
import yaml
import numpy
from copy import deepcopy

def read_datapath(datapath):
    """decode datapath from a yaml file"""
    with open(datapath, 'r') as sample_fid:
        datapath_config = yaml.safe_load(sample_fid)
    
    return datapath_config


def get_datetime_boundary(analysis_time_list, t0):
    """get the boundaries (t1 and t2)
    for the analysis time (t0)
    e.g., t1 <--> t0 <--> t2"""

    if t0 in analysis_time_list:
        return None

    dates = deepcopy(analysis_time_list)
    t1 = min(dates, key=lambda d: abs(d - t0))
    dates.remove(t1)
    t2 = min(dates, key=lambda d: abs(d - t0))
    
    return sorted([t1, t2])

def get_datetime_range(timelist):
    """get the start and end period for processing"""
    start_time = min(timelist)
    end_time = max(timelist)
    return start_time, end_time


def get_img_boundary(
        forecast, t_boundary, valid_dates):
    """get the associated forecast according to 
    its boundaries
        * prob_index indicate the index for prob dim, 
            e.g., the first dim of forecast usually 
            store the prob threshold of 25%
    """
    img1 = forecast[valid_dates.index(
        t_boundary[0]), :, :]
    img2 = forecast[valid_dates.index(
        t_boundary[1]), :, :]
    img_boundary = numpy.asarray([img1, img2])
    return img_boundary

def extract_raw_img(forecast, valid_times, analysis_time):
    """given the analysis time is within the list
    of original forecast time, return the original fcst"""
    fcst_index = valid_times.index(analysis_time)
    return forecast[fcst_index, :, :]


def create_dirs(output_dir):
    """create required directories"""
    dirs = {}
    dirs['figure'] = os.path.join(output_dir, 'figure')
    dirs['output'] = os.path.join(output_dir, 'output')
    
    for dir_name in dirs:
        if not os.path.exists(dirs[dir_name]):
            os.makedirs(dirs[dir_name])
    
    return dirs
    
    
        