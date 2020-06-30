import os
import dask
from datetime import timedelta

from utils import utils
from interp import temporal_interp
from data import oi


def run_interp(valid_times, cur_time, forecast):
    """run the actual temporal downscaling"""
    t_boundary = utils.get_datetime_boundary(
        valid_times, cur_time)
    if t_boundary is None:
        fcst = utils.extract_raw_img(
            forecast, valid_times, cur_time, prob_index=0)
        return cur_time, fcst

    img_boundary = utils.get_img_boundary(
        forecast, t_boundary, valid_times,
        prob_index=0)
    r = temporal_interp.t_interp(
        t_boundary, img_boundary, cur_time)
    return cur_time, r

def t_interp_wrapper(start_time, end_time, valid_times,
                     output_dir, datatype,
                     forecasts, mask_data, latitude, longitude,
                     target_interval_min):
    """control the temporal interp workflow"""
    
    interpolated_fcst = []
    interpolated_time = []
    dask_interp_jobs = []
    
    cur_time = start_time
    while cur_time <= end_time:
        dask_interp_jobs.append(dask.delayed(run_interp)(
            valid_times, cur_time, forecasts))
        cur_time += timedelta(
            seconds=60*target_interval_min)
    dask_outs = dask.compute(
        *dask_interp_jobs, scheduler='multiprocessing')
    for dask_out in dask_outs:
        interpolated_time.append(dask_out[0])
        interpolated_fcst.append(dask_out[1])
    
    output_path = os.path.join(
        output_dir, '{datatype}_from_{start_time}_to_{end_time}'.format(
            datatype=datatype, start_time=start_time.strftime('%Y%m%d%H%M'),
            end_time=end_time.strftime('%Y%m%d%H%M'))
        )
    
    oi.write_output(output_path, interpolated_fcst, latitude, 
                    longitude, interpolated_time, 
                    data_mask_in=mask_data)
