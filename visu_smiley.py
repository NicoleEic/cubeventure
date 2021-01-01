import numpy as np
import os
import cubeventure as cv

visu_name = 'smiley'
i_grid = 7

vols_max = 100

# initialize matrix
data_matrix = np.zeros((i_grid, i_grid, i_grid))

mid_slice = np.array([[0, 1, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 1],
                      [1, 1, 0, 0, 0, 1, 1],
                      [0, 1, 1, 1, 1, 1, 0],
                      [0, 0, 1, 1, 1, 0, 0]])

data_matrix[2, :, :] = np.rot90(mid_slice, k=3)
data_matrix[4, :, :] = np.rot90(mid_slice, k=3)

### save matrix
cv.save_matrix(data_matrix, visu_name)

# call visualization script
os.system(f'python plot_visualization.py {visu_name}')


