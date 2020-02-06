#source: https://github.com/ARM-DOE/pyart/blob/master/pyart/core/transforms.py

import warning
import numpy as np

def geographic_to_cartesian_aeqd(lon, lat, lon_0, lat_0, R=6370997.):
    """
    Azimuthal equidistant geographic to Cartesian coordinate transform.
    Transform a set of geographic coordinates (lat, lon) to
    Cartesian/Cartographic coordinates (x, y) using a azimuthal equidistant
    map projection [1]_.
    .. math::
        x = R * k * \\cos(lat) * \\sin(lon - lon_0)
        y = R * k * [\\cos(lat_0) * \\sin(lat) -
                     \\sin(lat_0) * \\cos(lat) * \\cos(lon - lon_0)]
        k = c / \\sin(c)
        c = \\arccos(\\sin(lat_0) * \\sin(lat) +
                     \\cos(lat_0) * \\cos(lat) * \\cos(lon - lon_0))
    Where x, y are the Cartesian position from the center of projection;
    lat, lon the corresponding latitude and longitude; lat_0, lon_0 are the
    latitude and longitude of the center of the projection; R is the radius of
    the earth (defaults to ~6371 km).
    Parameters
    ----------
    lon, lat : array-like
        Longitude and latitude coordinates in degrees.
    lon_0, lat_0 : float
        Longitude and latitude, in degrees, of the center of the projection.
    R : float, optional
        Earth radius in the same units as x and y. The default value is in
        units of meters.
    Returns
    -------
    x, y : array
        Cartesian coordinates in the same units as R, typically meters.
    References
    ----------
    .. [1] Snyder, J. P. Map Projections--A Working Manual. U. S. Geological
        Survey Professional Paper 1395, 1987, pp. 191-202.
    """
    lon = np.atleast_1d(np.asarray(lon))
    lat = np.atleast_1d(np.asarray(lat))

    lon_rad = np.deg2rad(lon)
    lat_rad = np.deg2rad(lat)

    lat_0_rad = np.deg2rad(lat_0)
    lon_0_rad = np.deg2rad(lon_0)

    lon_diff_rad = lon_rad - lon_0_rad

    # calculate the arccos after ensuring all values in valid domain, [-1, 1]
    arg_arccos = (np.sin(lat_0_rad) * np.sin(lat_rad) +
                  np.cos(lat_0_rad) * np.cos(lat_rad) * np.cos(lon_diff_rad))
    arg_arccos[arg_arccos > 1] = 1
    arg_arccos[arg_arccos < -1] = -1
    c = np.arccos(arg_arccos)
    with warnings.catch_warnings():
        # division by zero may occur here but is properly addressed below so
        # the warnings can be ignored
        warnings.simplefilter("ignore", RuntimeWarning)
        k = c / np.sin(c)
    # fix cases where k is undefined (c is zero), k should be 1
    k[c == 0] = 1

    x = R * k * np.cos(lat_rad) * np.sin(lon_diff_rad)
    y = R * k * (np.cos(lat_0_rad) * np.sin(lat_rad) -
                 np.sin(lat_0_rad) * np.cos(lat_rad) * np.cos(lon_diff_rad))
    return x, y