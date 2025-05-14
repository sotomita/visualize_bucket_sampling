#! /usr/bin/env/python3
# -*- encoding utf-8 -*-

import numpy as np

# plot area [lon_min,lon_max,lat_min,lat_max]
plot_area = [142, 145, 37, 42]

# interpolation
lon = np.arange(141, 146, 0.05)
lat = np.arange(36, 43, 0.05)
lon2d, lat2d = np.meshgrid(lon, lat)

# SST colorbar
sst_min = 5.0
sst_max = 16.0
sst_delta = 1.0

# norm of grad of SST colorbar
grad_min = 0.25
grad_max = 2.0
grad_delta = 0.125
