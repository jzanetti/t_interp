from mpl_toolkits.basemap import Basemap

def get_basemap(grid, llcrnrlon=160, urcrnrlon=180, llcrnrlat=-50, urcrnrlat=-30, res='i'):
    if grid is not None:
        llcrnrlon = grid['lons'][0]
        urcrnrlon = grid['lons'][1]
        llcrnrlat = grid['lats'][1]
        urcrnrlat = grid['lats'][0]

    map_obj = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, 
                      urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, 
                      projection='mill', resolution=res)
    return map_obj