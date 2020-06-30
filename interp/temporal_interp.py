import numpy
from pysteps import motion
from pysteps import nowcasts

def get_t_weights(analysis_time, t_boundary):
    """get the weights of analysis against boundaries
        * the final weights have to be opposite, e.g., 
        the smaller the distance between t0 and tstart, 
        the higher weight to be assigned
    """
    tstart2t0 = (analysis_time - t_boundary[0]).total_seconds()
    t02tend = (t_boundary[1] - analysis_time).total_seconds()
    t_total = tstart2t0 + t02tend
    tstart2t0_weight = tstart2t0/t_total
    t02tend_weight = t02tend/t_total
    
    return [t02tend_weight, tstart2t0_weight]


def get_mean_uv(uv_forward, uv_backward):
    """get mean uv from forward and backward uv"""
    u_forward = (uv_forward[0, :, :] - uv_backward[0, :, :])/2.0
    v_forward = (uv_forward[1, :, :] - uv_backward[1, :, :])/2.0
    u_backward = (uv_backward[0, :, :] - uv_forward[0, :, :])/2.0
    v_backward = (uv_backward[1, :, :] - uv_forward[1, :, :])/2.0
    uv_forward = numpy.asarray([u_forward, v_forward])
    uv_backward = numpy.asarray([u_backward, v_backward])
    return uv_forward, uv_backward


def t_interp(t_boundary, img_boundary, analysis_time):
    """interpolate the two images temporally"""
    tstart2t0_weight, t02tend_weight = \
        get_t_weights(analysis_time, t_boundary)
    dense_lucaskanade = motion.get_method('LK')
    uv_forward = dense_lucaskanade(
        img_boundary)
    uv_backward = dense_lucaskanade(
        img_boundary[::-1, :, :])
    uv_forward, uv_backward = get_mean_uv(uv_forward, uv_backward)
    
    extrapolate = nowcasts.get_method('extrapolation')
    r_from_tstart = extrapolate(img_boundary[0, :, :], 
                                uv_forward*t02tend_weight, 1)[0, :, :]
    r_from_tend = extrapolate(img_boundary[1, :, :], 
                              uv_backward*tstart2t0_weight, 1)[0, :, :]
    
    r = r_from_tstart*tstart2t0_weight + \
        r_from_tend*t02tend_weight

    return r
    