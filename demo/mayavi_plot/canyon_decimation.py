# Author: Gael Varoquaux <gael.varoquaux@normalesup.org>
# Copyright (c) 2008-2020, Enthought, Inc.
# License: BSD Style.

# Retrieve the grand Canyon topological data ###################################
# Original file:
#'ftp://e0srp01u.ecs.nasa.gov/srtm/version2/SRTM1/Region_04/N36W113.hgt.zip'
import os
if not os.path.exists('N36W113.hgt.zip'):
    # Download the data
    try:
        from urllib import urlopen
    except ImportError:
        from urllib.request import urlopen
    print('Downloading data, please wait (10M)')
    opener = urlopen(
    'https://s3.amazonaws.com/storage.enthought.com/www/sample_data/N36W113.hgt.zip'
        )
    open('N36W113.hgt.zip', 'wb').write(opener.read())

# Load the data (signed 2 byte integers, big endian) ###########################
import zipfile
import numpy as np

data = np.fromstring(zipfile.ZipFile('N36W113.hgt.zip').read('N36W113.hgt'),
                    '>i2')
data.shape = (3601, 3601)
data = data[200:400, 1200:1400]
data = data.astype(np.float32)

# Plot an interecting section ##################################################
from mayavi import mlab
mlab.figure(1, size=(450, 390))
mlab.clf()
data = mlab.pipeline.array2d_source(data)

# Use a greedy_terrain_decimation to created a decimated mesh
terrain = mlab.pipeline.greedy_terrain_decimation(data)
terrain.filter.error_measure = 'number_of_triangles'
terrain.filter.number_of_triangles = 5000
terrain.filter.compute_normals = True

# Plot it black the lines of the mesh
lines = mlab.pipeline.surface(terrain, color=(0, 0, 0),
                                      representation='wireframe')
# The terrain decimator has done the warping. We control the warping
# scale via the actor's scale.
lines.actor.actor.scale = [1, 1, 0.2]

# Display the surface itself.
surf = mlab.pipeline.surface(terrain, colormap='gist_earth',
                                      vmin=1450, vmax=1650)
surf.actor.actor.scale = [1, 1, 0.2]

# Display the original regular grid. This time we have to use a
# warp_scalar filter.
warp = mlab.pipeline.warp_scalar(data, warp_scale=0.2)
grid = mlab.pipeline.surface(warp, color=(1, 1, 1),
                                      representation='wireframe')

mlab.view(-17, 46, 143, [1.46, 8.46, 269.4])

mlab.show()