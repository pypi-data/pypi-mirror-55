import numpy as np
from . import detectors


def get_norm_det(net, ra, dec, psi, phi, cosi, t_gps):
    ''' Return the normalization to scale SNR from face-on to random sky-location for the network'''
    f_plus, f_cross = detectors.get_fp_fc(net, ra, dec, psi, t_gps)
    norm_det = detectors.norm_optsnr(net, phi, cosi, f_plus, f_cross)
    return norm_det

def generate_extrinsic_sky(n=1, ra_min=0, ra_max=2 * np.pi, sindec_min=-1, sindec_max=1):
    """
    Generate extrinsic parameters of an event
    """
    ra = np.random.uniform(ra_min, ra_max, size=n)
    dec = np.arcsin(np.random.uniform(sindec_min, sindec_max, size=n))
    return ra, dec

def generate_extrinsic_loc(n=1, lumd_min=0, lumd_max=5000, cosi_min=-1, cosi_max=1):
    """
    Generate extrinsic parameters of an event
    """
    lumd = (np.random.uniform(lumd_min ** 3, lumd_max ** 3, size = n)) ** (1/3.)
    cosi = np.random.uniform(cosi_min, cosi_max, size = n)
    return lumd, cosi
