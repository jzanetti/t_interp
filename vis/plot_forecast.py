import os
from vis import plot_map
from vis import color_ctl
import matplotlib.pyplot as plt

def plot_forecasts(fcst, latitude, longitude, fcst_time, datatype, 
                   outdir, colorscale='pysteps',
                   colorbar_shrink=0.45):
    """plot forecast"""
    plt.figure(figsize=(10, 15))
    filename = '{datatype}_{valid_time}.png'.format(
        datatype=datatype,
        valid_time=fcst_time.strftime('%Y%m%d%H%M'))
    filepath = os.path.join(outdir, filename)
    title_str = '{datatype}, {valid_time}'.format(
        datatype=datatype,  valid_time=fcst_time.strftime('%Y%m%d%H%M'))
    map_obj = plot_map.get_basemap(res='i')
    map_obj.drawcoastlines(linewidth=1.25)
    cmap, norm, clevs, _ = color_ctl.get_colormap('depth', 'mm/h', colorscale)
    x, y = map_obj(longitude, latitude)
    im = map_obj.pcolormesh(x, y, fcst, cmap=cmap, norm=norm, shading='gouraud')
    plt.colorbar(im, ticks=clevs, spacing='uniform', norm=norm,
            extend="max" if type in ["intensity", "depth"] else "neither",
            shrink=colorbar_shrink)
    if title_str:
        plt.title(title_str)
        
    plt.savefig(filepath, bbox_inches = 'tight')
    plt.close()
