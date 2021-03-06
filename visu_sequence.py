import os
import cubeventure as cv
import numpy as np

visu_name = 'sequence'
i_grid = 3

n_vols = i_grid ** 3
data_in = np.zeros((i_grid, i_grid, i_grid, n_vols))
i = 0
for i_x in np.arange(i_grid):
    for i_y in np.arange(i_grid):
        for i_z in np.arange(i_grid):
            data_in[:, :, :, i] = 0
            data_in[i_x, i_y, i_z, i] = 1
            i = i + 1

data_in = data_in.astype(np.int32)
cv.save_matrix(data_in, visu_name)

# call visualization script
os.system(f'python3 visualization_wrapper.py --fname {visu_name} --vis_type cube --time_step 0.5')
