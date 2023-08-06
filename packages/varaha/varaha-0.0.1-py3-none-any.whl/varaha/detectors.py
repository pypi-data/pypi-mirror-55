import numpy as np
import lal, lalsimulation
from astropy.time import Time
from astropy import constants
from pycbc.detector import Detector

def get_fp_fc(network, ra, dec, psi, t_gps):
    
    f_plus, f_cross = {}, {}
    
    for det in network:
        fp, fc = antenna_pattern(det, ra, dec, psi, t_gps)
        f_plus[det], f_cross[det] = np.array(fp), np.array(fc)
    
    return f_plus, f_cross


def norm_optsnr(net, phi, cosi, f_plus, f_cross):
    
    norm, angle = {}, {}

    for det in net:
        norm[det] = (np.cos(2 * phi) + 1j * np.sin(2 * phi))
        norm[det] *= (f_plus[det] * (1 + cosi ** 2) / 2 - 1j * f_cross[det] * cosi)
             
    return norm


def time_delay_between_obs(det1, det2, ra, dec, t_gps):
    D1, D2 = Detector(det1), Detector(det2)
    dt = D1.time_delay_from_detector(D2, ra, dec, t_gps * np.ones_like(ra))
    
    return dt


def antenna_pattern(det, right_ascension, declination, polarization, t_gps):
    """Return the detector response.

    Parameters
    ----------
    right_ascension: float or numpy.ndarray
        The right ascension of the source
    declination: float or numpy.ndarray
        The declination of the source
    polarization: float or numpy.ndarray
        The polarization angle of the source

    Returns
    -------
    fplus: float or numpy.ndarray
        The plus polarization factor for this sky location / orientation
    fcross: float or numpy.ndarray
        The cross polarization factor for this sky location / orientation
    """
    gmst = Time(t_gps, format='gps', location=(0, 0))
    gha = gmst.sidereal_time('mean').rad - right_ascension

    cosgha = np.cos(gha)
    singha = np.sin(gha)
    cosdec = np.cos(declination)
    sindec = np.sin(declination)
    cospsi = np.cos(polarization)
    sinpsi = np.sin(polarization)

    x0 = -cospsi * singha - sinpsi * cosgha * sindec
    x1 = -cospsi * cosgha + sinpsi * singha * sindec
    x2 =  sinpsi * cosdec
    x = np.array([x0, x1, x2])

    dx = lalsimulation.DetectorPrefixToLALDetector(det).response.dot(x)

    y0 =  sinpsi * singha - cospsi * cosgha * sindec
    y1 =  sinpsi * cosgha + cospsi * singha * sindec
    y2 =  cospsi * cosdec
    y = np.array([y0, y1, y2])
    dy = lalsimulation.DetectorPrefixToLALDetector(det).response.dot(y)

    if hasattr(dx, 'shape'):
        fplus = (x * dx - y * dy).sum(axis=0)
        fcross = (x * dy + y * dx).sum(axis=0)
    else:
        fplus = (x * dx - y * dy).sum()
        fcross = (x * dy + y * dx).sum()

    return fplus, fcross


class Detector(object):
    """A gravitational wave detector
    """
    def __init__(self, detector_name):
        self.name = str(detector_name)
        self.frDetector =  lalsimulation.DetectorPrefixToLALDetector(self.name)
        self.response = self.frDetector.response
        self.location = self.frDetector.location
        self.latitude = self.frDetector.frDetector.vertexLatitudeRadians
        self.longitude = self.frDetector.frDetector.vertexLongitudeRadians

    def time_delay_from_location(self, other_location, right_ascension,
                                 declination, t_gps):
        """Return the time delay from the given location to detector for
        a signal with the given sky location

        In other words return `t1 - t2` where `t1` is the
        arrival time in this detector and `t2` is the arrival time in the
        other location.

        Parameters
        ----------
        other_location : numpy.ndarray of coordinates
            A detector instance.
        right_ascension : float
            The right ascension (in rad) of the signal.
        declination : float
            The declination (in rad) of the signal.
        t_gps : float
            The GPS time (in s) of the signal.

        Returns
        -------
        float
            The arrival time difference between the detectors.
        """
        gmst = Time(t_gps, format='gps', location=(0, 0)).sidereal_time('mean').rad
        ra_angle = gmst - right_ascension
        cosd = np.cos(declination)

        e0 = cosd * np.cos(ra_angle)
        e1 = cosd * -np.sin(ra_angle)
        e2 = np.sin(declination)

        ehat = np.array([e0, e1, e2])
        dx = other_location - self.location
        return dx.dot(ehat) / constants.c.value


    def time_delay_from_detector(self, other_detector, right_ascension,
                                 declination, t_gps):
        """Return the time delay from the given to detector for a signal with
        the given sky location; i.e. return `t1 - t2` where `t1` is the
        arrival time in this detector and `t2` is the arrival time in the
        other detector. Note that this would return the same value as
        `time_delay_from_earth_center` if `other_detector` was geocentric.

        Parameters
        ----------
        other_detector : detector.Detector
            A detector instance.
        right_ascension : float
            The right ascension (in rad) of the signal.
        declination : float
            The declination (in rad) of the signal.
        t_gps : float
            The GPS time (in s) of the signal.

        Returns
        -------
        float
            The arrival time difference between the detectors.
        """
        return self.time_delay_from_location(other_detector.location,
                                             right_ascension,
                                             declination,
                                             t_gps)

