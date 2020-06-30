from mpl_toolkits.basemap import Basemap

def get_basemap(llcrnrlon=160, urcrnrlon=180, llcrnrlat=-50, urcrnrlat=-30, res='i'):
    map_obj = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, 
                      urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, 
                      projection='mill', resolution=res)
    return map_obj