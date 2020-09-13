from pyresample import geometry, image

def grid_interpolation(src_grid, tar_grid,
                       radius_of_influence=500000,
                       fill_value=None):
    src_lat = src_grid['lat']
    src_lon = src_grid['lon']
    src_data = src_grid['data']

    tar_lat = tar_grid['lat']
    tar_lon = tar_grid['lon']

    src_lon = src_lon % 360.0
    tar_lon = tar_lon % 360.0

    src_grid_def = geometry.GridDefinition(
                        lons=src_lon, lats=src_lat)
    tar_grid_def = geometry.GridDefinition(
                        lons=tar_lon, lats=tar_lat)
    src_img_container = image.ImageContainerNearest(
        src_data, src_grid_def, radius_of_influence=radius_of_influence,
                    fill_value=fill_value)
    tar_data = src_img_container.resample(tar_grid_def)

    return tar_data.image_data