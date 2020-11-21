import numpy as np
import os

# data path
dd = os.path.join(os.path.dirname(__file__), 'sequences')

# output filename
fname = os.path.join(dd, 'sequence')

i_grid = 7

n_vols = i_grid ** 3
data_in = np.zeros((i_grid, i_grid, i_grid, n_vols))
i_all = 0
for i_x in np.arange(i_grid):
    for i_y in np.arange(i_grid):
        for i_z in np.arange(i_grid):
            data_in[:, :, :, i_all] = 0
            data_in[i_x, i_y, i_z, i_all] = 1
            i_all = i_all + 1

np.save(fname, data_in)
