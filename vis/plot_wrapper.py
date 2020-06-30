import os
import dask
from vis import plot_forecast
from data import T_INTERP_FILENAME
from data import read_data

def plot_wrapper(datatype, figure_dir,
                 output_dir, start_time, end_time):
    
    output_path = os.path.join(
        output_dir, T_INTERP_FILENAME.format(
        datatype=datatype, start_time=start_time.strftime('%Y%m%d%H%M'),
        end_time=end_time.strftime('%Y%m%d%H%M')))
    
    forecast, forecast_times, latitude, longitude, data_mask = \
        read_data.read_interp_data(output_path, datatype)
    
    dask_plot_jobs = []
    for i, fcst_time in enumerate(forecast_times):
        dask_plot_jobs.append(
            dask.delayed(plot_forecast.plot_forecasts)(
                forecast[i, :, :], latitude, longitude, 
                fcst_time, datatype, figure_dir,
                data_mask=data_mask))

    dask.compute(
        *dask_plot_jobs, scheduler='multiprocessing')