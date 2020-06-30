import dask
from vis import plot_forecast


def plot_wrapper(interpolated_fcst, interpolated_time,
                 latitude, longitude, datatype, figure_dir):
    
    dask_plot_jobs = []
    for i, fcst in enumerate(interpolated_fcst):
        dask_plot_jobs.append(
            dask.delayed(plot_forecast.plot_forecasts)(
                fcst, latitude, longitude, 
                interpolated_time[i], 
                datatype, figure_dir))

    dask_outs = dask.compute(
        *dask_plot_jobs, scheduler='multiprocessing')