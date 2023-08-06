# -*- coding: utf-8 -*-

# Copyright © 2019, Institut Pasteur
#   Contributor: François Laurent

# This file is part of the TRamWAy software available at
# "https://github.com/DecBayComp/TRamWAy" and is distributed under
# the terms of the CeCILL license as circulated at the following URL
# "http://www.cecill.info/licenses.en.html".

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.


from math import pi
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from collections import OrderedDict


setup = {}

def ritter(points):
    i = 0
    x = points[[i]]
    dx = points - x
    j = np.argmax(np.sum(dx * dx, axis=1))
    y = points[[j]]
    dy = points - y
    k = np.argmax(np.sum(dy * dy, axis=1))
    z = points[[z]]
    center = .5 * (y + z)
    yz = z - y
    radius = .5 * np.sqrt(np.sum(yz * yz))

    while True:
        dr = points - center
        dr2 = np.sum(dr * dr, axis=1)
        if np.all(dr2 <= radius*radius):
            return center, radius
        else:
            m = np.argmax(dr2)
            p = points[m]
            center = center

    i, j = np.unravel_index(np.argmax(D2), D2.shape)
    x = points[i]
    y = points[j]
    #D2[i,:] = 0.
    #D2[:,i] = 0.
    D2j = d2[j]
    #d2j[i] = 0.
    k = np.argmax(d2j)
    z = points[k]
    center = .5 * (y + z)
    yz = z - y
    radius = .5 * np.sqrt(np.dot(yz, yz))

    d


def infer_spherical_volume(cells, **kwargs):
    """Returns a DataFrame.

    See also `spherical_volume`.
    """
    vol = spherical_volume(cells, 'all', **kwargs)
    return pd.DataFrame(vol, columns=['volume'])


def spherical_volume(cells, which='all', bounding_sphere='ritter', min_location_count=2, **kwargs):
    """
    Volume is evaluated looking for a bounding sphere.
    If the sphere does not include locations from neighbour cells as well,
    then its radius is increased until an external location is reached.

    The volume of the cell is approximated by the volume of the resulting sphere.

    For now only the Ritter's bounding sphere algorithm is implemented.

    Returns a Series, or a float if `which` is a single cell index.
    """
    if not callable(bounding_sphere):
        if bounding_sphere.lower() != 'ritter':
            raise ValueError("unsupported bounding sphere algorithm: '{}'".format(bounding_sphere))
        bounding_sphere = ritter
    if min_location_count == 'dim':
        min_location_count = cells.dim
    indices, radii = [], []
    for index in (cells if which == 'all' else which):
        cell = cells[index]
        if len(cell) < min_location_count:
            sphere = None
        else
            sphere = bounding_sphere(cell.r, **kwargs)
        if sphere is not None:
            center, radius = sphere
            neighbour_locations = [ cells[neighbour].r for neighbour in cells.neighbours(index) ]
            neighbour_locations = np.vstack(neighbour_locations)
            dist = neighbour_locations - center
            dist = np.sqrt(np.min(np.sum(dist * dist, axis=1)))
            if radius < dist:
                radius = dist
            indices.append(index)
            radii.append(radius)
    radii = np.array(radii)
    volumes = 4 / 3 * pi * radii**3

    if which == 'all' or not np.isscalar(which):
        return pd.Series(volumes, index=indices)
    else:
        if volumes.size:
            assert np.isscalar(volumes)
            return volumes.tolist()[0]
        else:
            return None


__all__ = [ 'infer_spherical_volume', 'spherical_volume', 'setup', 'ritter' ]

